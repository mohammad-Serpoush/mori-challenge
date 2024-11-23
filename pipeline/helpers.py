import json
import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import NotFoundException

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")


def load_data(count: int = 100, from_index: int = 0):

    with open("products.json", "r") as file:
        data = json.load(file)
    if from_index > len(data):
        raise IndexError

    return data[from_index:count]


def get_pinecone_index(name: str):

    client = Pinecone(
        api_key=PINECONE_API_KEY,
    )
    try:
        index = client.Index(name)
        print("Index exists")
    except NotFoundException:
        print("Index not exists")

        client.create_index(
            name,
            dimension=512,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print("Index not created")

        index = client.Index(name)
    return index


def get_metadata(row):
    return dict(
        category_name=row.get("category_name") or "",
        category_id=row.get("category_id") or 0,
        shop_id=row.get("shop_id") or 0,
        shop_name=row.get("shop_name") or "",
        link=row.get("link") or "",
        status=row.get("status") or "",
        region=row.get("region") or "",
        images=row.get("images") or [],
        name=row.get("name") or "",
        pid=row.get("id"),
        price=row.get("current_price", 0) or 0,
    )
