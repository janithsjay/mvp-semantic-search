#!/bin/bash
# ==========================================
# MVP Semantic Search Setup Script (Safe pip + venv)
# ==========================================

# --------------------------
# Configuration
# --------------------------
ENV_NAME="mvp_semsearch"
PROJECT_DIR="$HOME/Projects/GIT/mvp-semantic-search"
PYTHON_CMD="python3.11"   # Make sure Python 3.11 is installed
ESSENTIAL_PKGS="numpy faiss-cpu sentence-transformers tiktoken streamlit"
OPTIONAL_PKGS="torch torchvision transformers scikit-learn jinja2 huggingface-hub"
MIN_DISK_GB=5

# --------------------------
# 1️⃣ Check Python
# --------------------------
if ! command -v $PYTHON_CMD &>/dev/null; then
    echo "❌ Python 3.11 not found."
    echo "👉 Install it using: brew install python@3.11"
    exit 1
fi
echo "✅ Python detected: $($PYTHON_CMD --version)"

# --------------------------
# 2️⃣ Check free disk space
# --------------------------
FREE_GB=$(df -BG "$PROJECT_DIR" | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$FREE_GB" -lt "$MIN_DISK_GB" ]; then
    echo "❌ Not enough free disk space ($FREE_GB GB). Need at least $MIN_DISK_GB GB."
    exit 1
fi
echo "✅ Free disk space: $FREE_GB GB"

# --------------------------
# 3️⃣ Remove old virtual environment if exists
# --------------------------
if [ -d "$PROJECT_DIR/$ENV_NAME" ]; then
    echo "🗑 Removing old virtual environment..."
    rm -rf "$PROJECT_DIR/$ENV_NAME"
fi

# --------------------------
# 4️⃣ Create new virtual environment
# --------------------------
echo "🐍 Creating virtual environment..."
cd "$PROJECT_DIR" || exit
$PYTHON_CMD -m venv $ENV_NAME

# --------------------------
# 5️⃣ Activate environment
# --------------------------
echo "🔹 Activating environment..."
source "$PROJECT_DIR/$ENV_NAME/bin/activate"

# --------------------------
# 6️⃣ Upgrade pip
# --------------------------
pip install --upgrade pip wheel setuptools

# --------------------------
# 7️⃣ Install essential packages first
# --------------------------
echo "📦 Installing essential packages..."
pip install $ESSENTIAL_PKGS || { echo "❌ Failed installing essentials"; exit 1; }

# --------------------------
# 8️⃣ Install optional packages
# --------------------------
echo "📦 Installing optional packages (may take space/time)..."
pip install $OPTIONAL_PKGS || echo "⚠️ Some optional packages failed to install, you can retry later"

# --------------------------
# 9️⃣ Verify numpy & FAISS
# --------------------------
echo "🔍 Verifying FAISS and numpy..."
python - <<PYTHON_CHECK
import numpy
import faiss
d = 384
index = faiss.IndexFlatIP(d)
x = numpy.random.rand(2, d).astype("float32")
index.add(x)
distances, indices = index.search(x, 1)
print("✅ numpy and FAISS loaded successfully! Indices:", indices)
PYTHON_CHECK

# --------------------------
# 10️⃣ Final instructions
# --------------------------
echo "🎉 Setup complete!"
echo "💡 To activate environment anytime:"
echo "   source $PROJECT_DIR/$ENV_NAME/bin/activate"
echo "💡 Run your build_index.py and test_query.py scripts now."