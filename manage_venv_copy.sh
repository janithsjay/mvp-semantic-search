#!/bin/bash

# -----------------------------
# MVP Semantic Search Setup Script (venv + pip)
# -----------------------------

# Configuration
ENV_NAME="mvp_semsearch"
PYTHON_VERSION="3.11"
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/$ENV_NAME"

# -----------------------------
# 1️⃣ Check Python version
# -----------------------------
if ! command -v python$PYTHON_VERSION &>/dev/null; then
    echo "❌ Python $PYTHON_VERSION not found."
    echo "👉 Please install it (e.g., via pyenv or brew) before running this script."
    exit 1
fi

PYTHON_EXEC=python$PYTHON_VERSION

# -----------------------------
# 2️⃣ Remove existing venv if exists
# -----------------------------
if [ -d "$VENV_DIR" ]; then
    echo "🗑 Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# -----------------------------
# 3️⃣ Create virtual environment
# -----------------------------
echo "🐍 Creating virtual environment $ENV_NAME with Python $PYTHON_VERSION..."
$PYTHON_EXEC -m venv "$VENV_DIR"

# -----------------------------
# 4️⃣ Activate environment
# -----------------------------
echo "🔹 Activating virtual environment..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# -----------------------------
# 5️⃣ Upgrade pip
# -----------------------------
echo "📦 Upgrading pip..."
pip install --upgrade pip

# -----------------------------
# 6️⃣ Install required libraries
# -----------------------------
echo "📦 Installing libraries..."
pip install --upgrade \
    numpy \
    faiss-cpu \
    torch \
    torchvision \
    sentence-transformers==2.2.2 \
    "transformers<4.30" \
    "langchain>=0.0.200" \
    tiktoken \
    scikit-learn \
    "huggingface_hub<1.1.0" \
    streamlit \
    nltk \
    jinja2 \
    blinker

# -----------------------------
# 7️⃣ Final instructions
# -----------------------------
echo "🎉 Setup complete!"
echo "💡 To activate environment anytime:"
echo "   source $VENV_DIR/bin/activate"
echo "💡 Then run your scripts, e.g.:"
echo "   python -m streamlit run scripts/app.py  "