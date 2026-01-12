#!/bin/bash

# Script to download Grain RGB Dataset
# Usage: ./download_dataset.sh [URL]

set -e

# Default values
DATA_DIR="./data"
ZIP_FILE="Grain-Data-RGB.zip"
OUTPUT_DIR="Grain-Data-RGB"
DATASET_URL="${1:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if wget is installed
if ! command -v wget &> /dev/null; then
    print_error "wget is not installed. Please install it first."
    echo "On macOS: brew install wget"
    echo "On Ubuntu/Debian: sudo apt-get install wget"
    exit 1
fi

# Check if unzip is installed
if ! command -v unzip &> /dev/null; then
    print_error "unzip is not installed. Please install it first."
    echo "On macOS: unzip should be pre-installed"
    echo "On Ubuntu/Debian: sudo apt-get install unzip"
    exit 1
fi

# Create data directory
mkdir -p "$DATA_DIR"
cd "$DATA_DIR"

ZIP_PATH="$DATA_DIR/$ZIP_FILE"
EXTRACT_PATH="$DATA_DIR/$OUTPUT_DIR"

# Check if dataset already exists
if [ -d "$EXTRACT_PATH" ] && [ "$(ls -A $EXTRACT_PATH)" ]; then
    print_warn "Dataset directory $EXTRACT_PATH already exists."
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted."
        exit 0
    fi
    rm -rf "$EXTRACT_PATH"
fi

# Download dataset if URL is provided
if [ -n "$DATASET_URL" ]; then
    print_info "Downloading dataset from: $DATASET_URL"
    wget --progress=bar:force -O "$ZIP_FILE" "$DATASET_URL" || {
        print_error "Download failed!"
        exit 1
    }
    print_info "Download completed!"
elif [ ! -f "$ZIP_FILE" ]; then
    print_error "No URL provided and $ZIP_FILE not found in $DATA_DIR"
    echo ""
    echo "Usage:"
    echo "  ./download_dataset.sh <DATASET_URL>"
    echo ""
    echo "Example:"
    echo "  ./download_dataset.sh https://example.com/dataset.zip"
    echo ""
    echo "Or place $ZIP_FILE in $DATA_DIR and run:"
    echo "  ./download_dataset.sh"
    exit 1
else
    print_info "Using existing $ZIP_FILE"
fi

# Extract the zip file
if [ -f "$ZIP_FILE" ]; then
    print_info "Extracting $ZIP_FILE to $OUTPUT_DIR..."
    unzip -q "$ZIP_FILE" -d "$OUTPUT_DIR" || {
        print_error "Extraction failed!"
        exit 1
    }
    print_info "Extraction completed!"
    
    # Count .npz files
    NPZ_COUNT=$(find "$OUTPUT_DIR" -name "*.npz" | wc -l)
    print_info "Dataset ready at: $EXTRACT_PATH"
    print_info "Total .npz files: $NPZ_COUNT"
    
    # Optional: remove zip file after extraction
    read -p "Do you want to remove the zip file to save space? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$ZIP_FILE"
        print_info "Zip file removed."
    fi
else
    print_error "Zip file $ZIP_FILE not found!"
    exit 1
fi

print_info "Done!"
