# Grain Classification Challenge - M1 AI

A complete implementation for the Grain AI Challenge focusing on multi-class classification of grain varieties from RGB images.

## 📋 Overview

This project implements a deep learning solution for classifying grain varieties using RGB image data. The challenge involves:

- **Task**: Multi-class classification of grain varieties from RGB images
- **Data**: RGB images stored in `.npz` format with metadata in filenames
- **Model**: Convolutional Neural Network (CNN) for image classification
- **Evaluation**: Accuracy, precision, recall, and F1-score metrics

## 🎯 Challenge Details

### Data Structure

Each `.npz` file contains:

- `x`: RGB image array (H, W, 3)
- `y`: Label/target value (grain variety number)

Filenames contain metadata:

- `grainID`: Unique grain identifier
- `varietyNumber`: Grain variety class
- `microplotID`: Microplot coordinates (x, y)
- `timestamp`: Date and time information

### Model Architecture

The implementation uses a CNN architecture (`GrainCNN`) with:

- 4 convolutional layers with batch normalization
- Max pooling and adaptive pooling for variable image sizes
- Dropout regularization
- Fully connected layers for classification

## 🚀 Quick Start

### 1. Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Download Dataset

Download the dataset using the provided shell script:

```bash
# Make script executable (first time only)
chmod +x download_dataset.sh

# Download from URL
./download_dataset.sh <DATASET_URL>

# Or if you already have the zip file in ./data/, just extract it
./download_dataset.sh
```

The script will:

- Download the dataset zip file (if URL provided)
- Extract it to `./data/Grain-Data-RGB/`
- Show progress and file count
- Ask if you want to remove the zip file after extraction

### 3. Run the Notebooks

Open and run the Jupyter notebooks:

```bash
jupyter notebook src/read_grain_rgb_data.ipynb
```


## 🔧 Usage

### Training a Model

```python
from src.README import Data, Train, Visualize, Score

# Load data
data = Data(data_dir="./data/Grain-Data-RGB")
data.load_data()

# Visualize data
visualize = Visualize(data=data)
visualize.plot_data()

# Train model
train = Train(data=data, model_path="./models/grain_model.pth")
history = train.train(epochs=20, batch_size=32, learning_rate=0.001)

# Evaluate model
score = Score(model=train.model, data=data)
results = score.compute_score()
```

## 📁 Project Structure

```
Grain-Challenge-M1-AI/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── download_dataset.sh       # Dataset download script
├── data/                     # Dataset directory
│   ├── Grain-Data-RGB/      # Extracted dataset (after download)
└── src/                      # Source code
    └── read_grain_rgb_data.ipynb  # Data exploration notebook
```

---

For questions or issues, please refer to the notebook documentation or open an issue.
