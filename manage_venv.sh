#!/bin/bash
# ==========================================
# MVP Semantic Search Setup Script (Conda / Miniforge)
# ==========================================

# --------------------------
# Configuration
# --------------------------
ENV_NAME="mvp_semsearch"
PYTHON_VERSION="3.11"
PROJECT_DIR="$HOME/Projects/GIT/mvp-semantic-search"

# --------------------------
# 1️⃣ Check Conda / Miniforge
# --------------------------
if ! command -v conda &>/dev/null; then
    echo "❌ Conda/Miniforge not found. Please install it first: https://github.com/conda-forge/miniforge"
    exit 1
fi
echo "✅ Conda detected"

# --------------------------
# 2️⃣ Remove old environment if exists
# --------------------------
if conda env list | grep -q "^$ENV_NAME"; then
    echo "🗑 Removing old environment $ENV_NAME..."
    conda remove -y -n $ENV_NAME --all
fi

# --------------------------
# 3️⃣ Create new Conda environment
# --------------------------
echo "🐍 Creating new Conda environment $ENV_NAME with Python $PYTHON_VERSION..."
conda create -y -n $ENV_NAME python=$PYTHON_VERSION

# --------------------------
# 4️⃣ Activate environment
# --------------------------
echo "🔹 Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

# --------------------------
# 5️⃣ Install dependencies
# --------------------------
echo "📦 Installing FAISS + dependencies..."
# FAISS CPU via conda-forge (ensures matching binaries for macOS)
conda install -y -c conda-forge faiss-cpu numpy

# Python packages via pip
pip install --upgrade pip
pip install sentence-transformers==2.2.2 transformers==4.30.2 \
            nltk==3.8.1 spacy==3.6.0 langchain>=0.0.200 tiktoken

# --------------------------
# 6️⃣ Verify FAISS
# --------------------------
echo "🔍 Verifying FAISS..."
python - <<PYTHON_CHECK
import numpy
import faiss
d = 384
index = faiss.IndexFlatIP(d)
x = numpy.random.rand(2, d).astype("float32")
index.add(x)
distances, indices = index.search(x, 1)
print("✅ FAISS works! Indices:", indices)
PYTHON_CHECK

# --------------------------
# 7️⃣ Final instructions
# --------------------------
echo "🎉 Setup complete!"
echo "💡 To activate environment anytime:"
echo "   conda activate $ENV_NAME"
echo "💡 Run your build_index.py and test_query.py scripts now."