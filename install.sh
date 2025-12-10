#!/bin/bash
#
# install.sh: A user-friendly installer for the AI-DevTeam CLI
#

# --- Colors and Formatting ---
C_BLUE="\033[94m"
C_GREEN="\033[92m"
C_RED="\033[91m"
C_YELLOW="\033[93m"
C_RESET="\033[0m"

info() {
    echo -e "${C_BLUE}[INFO]${C_RESET} $1"
}

success() {
    echo -e "${C_GREEN}[SUCCESS]${C_RESET} $1"
}

error() {
    echo -e "${C_RED}[ERROR]${C_RESET} $1"
}

warn() {
    echo -e "${C_YELLOW}[WARNING]${C_RESET} $1"
}

# --- Installation Steps ---

# 1. Welcome and Check for root
info "Starting the AI-DevTeam CLI installer..."
if [ "$EUID" -eq 0 ]; then
  error "This script should not be run as root. Please run as a regular user."
  exit 1
fi

# 2. Check for dependencies
info "Checking for dependencies (python3, pip, venv)..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    error "Python3 and Pip are required. Please install them first."
    info "On Debian/Ubuntu, try: sudo apt update && sudo apt install python3-full python3-pip"
    exit 1
fi
success "Dependencies found."

# 3. Set up virtual environment
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    info "Creating Python virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        error "Failed to create virtual environment."
        exit 1
    fi
    success "Virtual environment created."
else
    info "Virtual environment already exists."
fi

# 4. Install the project in editable mode
info "Installing the project and its dependencies..."
"$VENV_DIR/bin/pip" install -e "$PROJECT_DIR"
if [ $? -ne 0 ]; then
    error "Installation failed."
    exit 1
fi
success "Project installed successfully."

# 5. Check and configure PATH
# pip places executables in ~/.local/bin for user installs
LOCAL_BIN_DIR="$HOME/.local/bin"
COMMAND_PATH="$LOCAL_BIN_DIR/team"

if ! command -v team &> /dev/null; then
    warn "The 'team' command is not on your PATH after installation."
    
    # Manually ensure the symbolic link exists
    info "Attempting to create the command link manually..."
    mkdir -p "$LOCAL_BIN_DIR" # Ensure the target directory exists
    ln -sf "$VENV_DIR/bin/team" "$COMMAND_PATH"
    if [ $? -ne 0 ]; then
        error "Failed to create a symbolic link for the 'team' command."
        info "Please try running this installer with sudo, or manually link '$VENV_DIR/bin/team' to a directory on your PATH."
        exit 1
    fi
    success "Manually created 'team' command link in '$LOCAL_BIN_DIR'."

    info "To make the command available, you need to add '$LOCAL_BIN_DIR' to your PATH."

    SHELL_CONFIG_FILE=""
    if [ -n "$BASH_VERSION" ] || [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG_FILE="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
        SHELL_CONFIG_FILE="$HOME/.zshrc"
    else
        warn "Could not determine your shell config file (.bashrc, .zshrc). You will need to add it manually."
    fi

    if [ -n "$SHELL_CONFIG_FILE" ]; then
        if ! grep -q "export PATH=\"$LOCAL_BIN_DIR:\$PATH\"" "$SHELL_CONFIG_FILE"; then
            info "I can add the following line to your $SHELL_CONFIG_FILE:"
            echo ""
            echo "    export PATH=\"$LOCAL_BIN_DIR:\$PATH\""
            echo ""
            read -p "Do you want to proceed? (y/N) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo -e "\n# Added by AI-DevTeam installer\nexport PATH=\"$LOCAL_BIN_DIR:\$PATH\"" >> "$SHELL_CONFIG_FILE"
                success "Added PATH to $SHELL_CONFIG_FILE."
                info "Please restart your terminal or run 'source $SHELL_CONFIG_FILE' to use the 'team' command."
            else
                warn "Please add '$LOCAL_BIN_DIR' to your PATH manually."
            fi
        else
            info "'$LOCAL_BIN_DIR' is already in your $SHELL_CONFIG_FILE, but the shell needs reloading."
            info "Please restart your terminal or run 'source $SHELL_CONFIG_FILE' to use the 'team' command."
        fi
    fi
else
    success "The 'team' command is already available!"
fi

echo ""
success "AI-DevTeam CLI installation complete!"
