"""
Run once locally to chunk, embed, and upload documents to Pinecone.

Setup:
  pip install pinecone google-generativeai

Usage:
  PINECONE_API_KEY=xxx GEMINI_API_KEY=xxx python scripts/embed_and_upload.py
"""

import os
import re
import time
from google import genai
from google.genai import types
from pinecone import Pinecone, ServerlessSpec

# ── Config ────────────────────────────────────────────────────────────────────
DOCS_PATH = "/Users/pinxiu/Document/resume/all_documents.txt"
PINECONE_INDEX = "pinxiu-portfolio"
CHUNK_SIZE = 800      # characters per chunk
CHUNK_OVERLAP = 150   # overlap between chunks

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# ── Parse documents ───────────────────────────────────────────────────────────
def parse_documents(path):
    with open(path, "r") as f:
        content = f.read()

    pattern = r"={30}\nDOCUMENT: (.+?)\n={30}\n(.*?)(?=\n={30}|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    docs = []
    for name, body in matches:
        docs.append({"name": name.strip(), "text": body.strip()})
    return docs

# ── Chunk text ────────────────────────────────────────────────────────────────
def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

# ── Embed with Gemini ─────────────────────────────────────────────────────────
def embed(client, text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return result.embeddings[0].values

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    client = genai.Client(api_key=GEMINI_API_KEY)

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if PINECONE_INDEX not in pc.list_indexes().names():
        print(f"Creating index '{PINECONE_INDEX}'...")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        time.sleep(10)

    index = pc.Index(PINECONE_INDEX)

    docs = parse_documents(DOCS_PATH)
    print(f"Parsed {len(docs)} documents")

    vectors = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        print(f"  {doc['name']}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue

            embedding = embed(client, chunk)
            vector_id = f"{doc['name']}__chunk{i}"

            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "source": doc["name"],
                    "text": chunk,
                }
            })

            time.sleep(0.3)  # stay within free tier rate limits

    # Upload in batches of 100
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"Uploaded batch {i // batch_size + 1} ({len(batch)} vectors)")

    print(f"\nDone. Total vectors uploaded: {len(vectors)}")
    stats = index.describe_index_stats()
    print(f"Index stats: {stats}")

if __name__ == "__main__":
    main()
