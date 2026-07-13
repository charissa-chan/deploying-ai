from dotenv import load_dotenv
import os
from openai import OpenAI
import chromadb
import uuid

# loading environment varaibles
load_dotenv(".env")
load_dotenv(".secrets")

#creating OpenAI client
client = OpenAI(
    base_url="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    api_key="any",
    default_headers={
        "x-api-key": os.getenv("API_GATEWAY_KEY")})


# Opening database file
with open("assignment_chat/data/curiosity_dataset.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Splitting data by separators.
facts = text.split("<sep>")

# Cleaning up extra spaces
cleaned_facts = []

for fact in facts:
    fact = fact.replace("\n", " ")
    fact = fact.strip()

    if fact:
        cleaned_facts.append(fact)

facts = cleaned_facts



# creating embeddings with persistent chromadb instance
chroma_client = chromadb.PersistentClient(path="./assignment_chat/chroma_db")

collection = chroma_client.get_or_create_collection(name="fun_facts")

response = client.embeddings.create(
    input=facts,
    model="text-embedding-3-small")

embeddings = [item.embedding for item in response.data]

ids = [f"id{i}" for i in range(len(facts))]

collection.add(
    embeddings=embeddings,
    documents=facts,
    ids=ids)