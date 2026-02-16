#!/bin/bash

################################################################################
# Stable Diffusion WebUI (Automatic1111) Installer for macOS Apple Silicon
# Includes ControlNet and ReActor extensions with critical Silicon fixes
################################################################################

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
}

################################################################################
# Step 1: Prerequisites Check
################################################################################

print_header "Step 1: Checking Prerequisites"

# Check if Homebrew is installed
print_status "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    print_error "Homebrew is not installed!"
    print_status "Please install Homebrew first by running:"
    echo ""
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
    exit 1
else
    print_success "Homebrew is installed ($(brew --version | head -n 1))"
fi

# Install required dependencies via Homebrew
print_status "Installing dependencies via Homebrew..."
print_status "This may take several minutes..."

dependencies=("cmake" "protobuf" "rust" "python@3.10" "git" "wget")

for dep in "${dependencies[@]}"; do
    print_status "Checking/Installing $dep..."
    if brew list "$dep" &> /dev/null; then
        print_success "$dep is already installed"
    else
        print_status "Installing $dep..."
        brew install "$dep" || {
            print_error "Failed to install $dep"
            exit 1
        }
        print_success "$dep installed successfully"
    fi
done

# Ensure Python 3.10 is available
print_status "Setting up Python 3.10..."
PYTHON_PATH=$(brew --prefix python@3.10)/bin/python3.10

if [ ! -f "$PYTHON_PATH" ]; then
    print_error "Python 3.10 not found at expected location: $PYTHON_PATH"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_PATH --version)
print_success "Using $PYTHON_VERSION"

################################################################################
# Step 2: Core Installation
################################################################################

print_header "Step 2: Installing Stable Diffusion WebUI"

# Set installation directory
INSTALL_DIR="stable-diffusion-webui"

# Clone the Automatic1111 repository
print_status "Cloning Automatic1111 repository..."
if [ -d "$INSTALL_DIR" ]; then
    print_warning "Directory '$INSTALL_DIR' already exists. Skipping clone."
    print_warning "If you want a fresh install, please remove this directory first."
else
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git "$INSTALL_DIR" || {
        print_error "Failed to clone Automatic1111 repository"
        exit 1
    }
    print_success "Repository cloned successfully"
fi

# Navigate to the installation directory
cd "$INSTALL_DIR" || {
    print_error "Failed to navigate to $INSTALL_DIR"
    exit 1
}

# Create Python virtual environment
print_status "Creating Python virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    $PYTHON_PATH -m venv venv || {
        print_error "Failed to create virtual environment"
        exit 1
    }
    print_success "Virtual environment created successfully"
fi

################################################################################
# Step 3: Critical Silicon Fixes (The "ReActor" Fix)
################################################################################

print_header "Step 3: Applying Critical Silicon Fixes"

# Activate the virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate || {
    print_error "Failed to activate virtual environment"
    exit 1
}

# Verify we're in the correct Python environment
print_status "Using Python: $(which python)"

# Upgrade pip, setuptools, and wheel
print_status "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel || {
    print_error "Failed to upgrade pip tools"
    exit 1
}
print_success "pip tools upgraded successfully"

# Install onnxruntime-silicon FIRST (critical for hardware acceleration)
print_status "Installing onnxruntime-silicon for Apple Silicon hardware acceleration..."
pip install onnxruntime-silicon || {
    print_error "Failed to install onnxruntime-silicon"
    exit 1
}
print_success "onnxruntime-silicon installed successfully"

# Install insightface manually (prevents "building wheel failed" error on macOS)
print_status "Installing insightface manually..."
pip install insightface || {
    print_error "Failed to install insightface"
    exit 1
}
print_success "insightface installed successfully"

################################################################################
# Step 4: Extensions Setup
################################################################################

print_header "Step 4: Installing Extensions"

# Create extensions directory if it doesn't exist
mkdir -p extensions

# Clone ControlNet extension
print_status "Installing ControlNet extension..."
if [ -d "extensions/sd-webui-controlnet" ]; then
    print_warning "ControlNet extension already exists. Skipping."
else
    git clone https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet || {
        print_error "Failed to clone ControlNet extension"
        exit 1
    }
    print_success "ControlNet extension installed successfully"
fi

# Clone ReActor extension
print_status "Installing ReActor extension..."
if [ -d "extensions/sd-webui-reactor" ]; then
    print_warning "ReActor extension already exists. Skipping."
else
    git clone https://github.com/Gourieff/sd-webui-reactor.git extensions/sd-webui-reactor || {
        print_error "Failed to clone ReActor extension"
        exit 1
    }
    print_success "ReActor extension installed successfully"
fi

################################################################################
# Step 5: Launcher Creation
################################################################################

print_header "Step 5: Creating Launcher Script"

# Create the run_mac.sh launcher script
print_status "Creating run_mac.sh launcher..."
cat > run_mac.sh << 'EOF'
#!/bin/bash

################################################################################
# Stable Diffusion WebUI Launcher for macOS Apple Silicon
################################################################################

# Activate virtual environment
source venv/bin/activate

# Launch WebUI with Mac-optimized arguments
python launch.py \
    --skip-torch-cuda-test \
    --no-half \
    --upcast-sampling \
    --use-cpu interrogate

EOF

# Make the launcher executable
chmod +x run_mac.sh || {
    print_error "Failed to make run_mac.sh executable"
    exit 1
}
print_success "run_mac.sh created and made executable"

################################################################################
# Installation Complete
################################################################################

print_header "Installation Complete! 🎉"

echo ""
print_success "Stable Diffusion WebUI with ControlNet and ReActor has been installed successfully!"
echo ""
print_status "Installation directory: $(pwd)"
echo ""
print_status "To start the application, run:"
echo ""
echo -e "  ${GREEN}cd $INSTALL_DIR${NC}"
echo -e "  ${GREEN}./run_mac.sh${NC}"
echo ""
print_status "The web interface will open automatically in your browser at:"
echo -e "  ${BLUE}http://127.0.0.1:7860${NC}"
echo ""
print_warning "Important Notes:"
echo "  • On first run, additional models and dependencies will be downloaded"
echo "  • This may take 10-30 minutes depending on your internet connection"
echo "  • Make sure you have at least 10GB of free disk space"
echo "  • The application is optimized for Apple Silicon (M1/M2/M3)"
echo ""
print_status "Extensions installed:"
echo "  ✓ ControlNet - Advanced image control and guidance"
echo "  ✓ ReActor - Face swapping capabilities"
echo ""
print_success "Happy creating! 🎨"
echo ""
