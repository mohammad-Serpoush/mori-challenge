from io import BytesIO

import requests
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from helpers import get_metadata, get_pinecone_index, load_data


def insert_data(batch_size: int = 20, row_counts: int = 100):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    data = load_data(row_counts)
    pinecone_index = get_pinecone_index("products")
    vectors = []

    for row_index, row in enumerate(data):
        images = row["images"]
        for index, image in enumerate(images):
            res = requests.get(image)
            image_ = Image.open(BytesIO(res.content))

            inputs = processor(images=image_, return_tensors="pt")
            with torch.no_grad():
                image_embeddings = list(model.get_image_features(**inputs))
            vectors.append(
                {
                    "values": image_embeddings[0],
                    "id": f"{row.get('id')}-{index}",
                    "metadata": {**get_metadata(row)},
                }
            )
        print(f"row no {row_index} was embedded.")
        if (row_index + 1) % batch_size == 0:
            print(f"Upsert {batch_size} rows")
            pinecone_index.upsert(vectors)
            print("Done!")
            vectors = []
    if vectors:
        pinecone_index.upsert(vectors)


if __name__ == "__main__":
    insert_data(20)
