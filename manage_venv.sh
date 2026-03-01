#!/bin/bash
# ========================================================
# Project-specific virtual environment manager
# Handles: setup, activate, deactivate
# ========================================================

# Name of the virtual environment
VENV_NAME="venv_mvp_semsearch"

# Python interpreter to use; override by setting PYTHON env var or editing here
PYTHON=${PYTHON:-python3.10.12}

# require at least python 3.11 for compatibility
required_major=3
required_minor=11
if ! $PYTHON -c "import sys; exit(0 if sys.version_info[:2] >= ($required_major,$required_minor) else 1)"; then
    echo "Error: $PYTHON must be >=${required_major}.${required_minor}." 1>&2
    exit 1
fi

# -----------------------------
# Function: setup
# -----------------------------
get_venv_python_version() {
    if [ -x "$VENV_NAME/bin/python" ]; then
        "$VENV_NAME/bin/python" -c 'import sys; print("%s.%s"%(sys.version_info.major,sys.version_info.minor))'
    fi
}

setup_venv() {
    if [ -d "$VENV_NAME" ]; then
        venv_ver=$(get_venv_python_version)
        echo "Virtual environment '$VENV_NAME' exists (python $venv_ver)."
        # if version mismatch, recreate
        desired_ver=$($PYTHON -c 'import sys; print("%s.%s"%(sys.version_info.major,sys.version_info.minor))')
        if [ "$venv_ver" != "$desired_ver" ]; then
            echo "Version mismatch: need python $desired_ver but venv has $venv_ver."
            echo "Removing and recreating venv."
            rm -rf "$VENV_NAME"
        fi
    fi

    if [ ! -d "$VENV_NAME" ]; then
        echo "Creating virtual environment '$VENV_NAME' with $PYTHON..."
        $PYTHON -m venv $VENV_NAME
        echo "Virtual environment created!"
    fi

    echo "Activating '$VENV_NAME'..."
    source $VENV_NAME/bin/activate

    echo "Upgrading pip and installing dependencies..."
    $VENV_NAME/bin/python -m pip install --upgrade pip
    $VENV_NAME/bin/python -m pip install -r ./requirements.txt  # paths relative to scripts/

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
