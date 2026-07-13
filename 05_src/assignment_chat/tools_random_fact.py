from langchain.tools import tool
import chromadb
import random


chroma_client = chromadb.PersistentClient(path="./assignment_chat/chroma_db")

collection = chroma_client.get_collection(name="fun_facts")


@tool
def get_random_fact():
    """
    Returns a random fun fact from the fun facts database.
    Use this when the user asks for a random fact or trivia.
    """

    results = collection.get(
        include=["documents"])
    fact = random.choice(results["documents"])
    return fact