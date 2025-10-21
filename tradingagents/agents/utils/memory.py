import chromadb
from chromadb.config import Settings
from openai import OpenAI
import os


class FinancialSituationMemory:
    def __init__(self, name, config):
        self.config = config
        
        # Initialize embedding model based on provider
        if config["llm_provider"].lower() == "ollama":
            # Use Ollama embeddings
            self.embedding = "nomic-embed-text"
            self.client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # Ollama doesn't require API key
        elif config["llm_provider"].lower() == "huggingface" and config.get("local_embeddings", False):
            # Use local HuggingFace embeddings
            self.embedding_model = None  # Will be initialized on first use
            self.client = None
        else:
            # Use OpenAI-compatible embeddings
            if config["backend_url"] == "http://localhost:11434/v1":
                self.embedding = "nomic-embed-text"
                self.client = OpenAI(base_url=config["backend_url"], api_key="ollama")
            else:
                self.embedding = "text-embedding-3-small"
                # Initialize client with API key from environment or config
                api_key = os.getenv("OPENAI_API_KEY") or config.get("openai_api_key")
                self.client = OpenAI(base_url=config["backend_url"], api_key=api_key)
        
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.create_collection(name=name)

    def get_embedding(self, text):
        """Get embedding for a text using appropriate provider"""
        
        if self.config["llm_provider"].lower() == "huggingface" and self.config.get("local_embeddings", False):
            # Use local HuggingFace embeddings
            if self.embedding_model is None:
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer(self.config.get("embedding_model", "all-MiniLM-L6-v2"))
            
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        else:
            # Use OpenAI-compatible embeddings
            response = self.client.embeddings.create(
                model=self.embedding, input=text
            )
            return response.data[0].embedding

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using OpenAI embeddings"""
        query_embedding = self.get_embedding(current_situation)

        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory()

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
