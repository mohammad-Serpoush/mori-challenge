import os
from pinecone import Pinecone
import meilisearch


def get_pinecone():
    return Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY"),
    )


def get_meilisearch():
    return meilisearch.Client(os.environ.get("MEILISEARCH_HOST") , os.environ.get("MEILISEARCH_API_KEY"))

