#!/bin/bash
# Download Sentence-BERT model weights and cache them

set -e

MODEL_DIR="./backend/models"
MODEL_NAME="sentence-transformers/all-mpnet-base-v2"

echo "Downloading Sentence-BERT model: $MODEL_NAME"

# Create models directory
mkdir -p "$MODEL_DIR"

# Use Python to download the model
python3 << EOF
from sentence_transformers import SentenceTransformer
import os

model_dir = os.path.expanduser("$MODEL_DIR")
model_name = "$MODEL_NAME"

print(f"Loading model: {model_name}")
model = SentenceTransformer(model_name, cache_folder=model_dir)
print(f"Model loaded and cached to: {model_dir}")
EOF

echo "Model download complete!"

