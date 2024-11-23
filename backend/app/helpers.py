from pinecone import Index
from transformers import CLIPProcessor, CLIPModel

import torch


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def fetch_relevant_vector(
    index: Index, text_description: str, top_k: int = 10, filters={}
):
    inputs = processor(text=[text_description], return_tensors="pt", padding=True)
    with torch.no_grad():
        text_embedding = model.get_text_features(**inputs)
    text_embedding = text_embedding.squeeze().tolist()
    response = index.query(
        namespace=None,
        vector=text_embedding,
        top_k=top_k,
        include_values=True,
        include_metadata=True,
        filter=filters,
    )

    return response
