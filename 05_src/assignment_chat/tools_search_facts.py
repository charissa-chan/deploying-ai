from langchain.tools import tool
import chromadb
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv(".env")
load_dotenv(".secrets")

openai_client = OpenAI(
    base_url="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    api_key="any",
    default_headers={
        "x-api-key": os.getenv("API_GATEWAY_KEY")
    })

# Connect to the existing persistent Chroma database
chroma_client = chromadb.PersistentClient(path="./assignment_chat/chroma_db")

collection = chroma_client.get_collection(name="fun_facts")


def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return openai_client.embeddings.create(input=[text], model=model).data[0].embedding


@tool
def search_facts(query: str):
    """
    Searches the fact database for facts related to a topic.
    """
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1)

    return results["documents"][0][0]