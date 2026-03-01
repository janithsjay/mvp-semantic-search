#!/bin/bash
# ========================================================
# Project-specific virtual environment manager
# Handles: setup, activate, deactivate
# ========================================================

# Name of the virtual environment
VENV_NAME="venv_mvp_semsearch"

# -----------------------------
# Function: setup
# -----------------------------
setup_venv() {
    if [ -d "$VENV_NAME" ]; then
        echo "Virtual environment '$VENV_NAME' already exists."
    else
        echo "Creating virtual environment '$VENV_NAME'..."
        python3 -m venv $VENV_NAME
        echo "Virtual environment created!"
    fi

    echo "Activating '$VENV_NAME'..."
    source $VENV_NAME/bin/activate

    echo "Upgrading pip and installing dependencies..."
    pip install --upgrade pip
    pip install -r ../requirements.txt  # Assuming script runs in scripts/

    echo "Setup complete! Virtual environment is active."
}

# -----------------------------
# Function: activate
# -----------------------------
activate_venv() {
    if [ -d "$VENV_NAME" ]; then
        source $VENV_NAME/bin/activate
        echo "Activated virtual environment '$VENV_NAME'"
    else
        echo "Virtual environment '$VENV_NAME' does not exist. Run './manage_venv.sh setup' first."
    fi
}

# -----------------------------
# Function: deactivate
# -----------------------------
deactivate_venv() {
    deactivate 2>/dev/null || echo "No virtual environment is active."
    echo "Virtual environment deactivated."
}

# -----------------------------
# Main
# -----------------------------
case "$1" in
    setup)
        setup_venv
        ;;
    activate)
        activate_venv
        ;;
    deactivate)
        deactivate_venv
        ;;
    *)
        echo "Usage: $0 {setup|activate|deactivate}"
        exit 1
        ;;
esac
