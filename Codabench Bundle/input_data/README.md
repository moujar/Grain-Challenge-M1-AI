# Input Data

**Note:** The actual data files are not included in this repository due to their large size (~560 MB). It has been added to the Starting Kit provided for participant

## Contents

This directory should contain:

1. **`.npz` files** - All grain image files (both training and test samples).
   Each `.npz` file contains:
   - `x`: grain image array of shape `(252, 252, 3)` (dtype `int16`)
   - `y`: variety label (string)
   - `original_filename`: original source filename
   - `bands`: spectral band indices used for the RGB representation

2. **`input_data.csv`** - A CSV file listing **only the training samples** with the following columns:
   - `filename`: the `.npz` filename (e.g., `grain7795_x40y20-var6_8000_us_2x_2020-12-02T134036_corr.npz`)
   - `varietyNumber`: the grain variety label (integer, 1-8)

Test samples are `.npz` files present in this directory but **not** listed in `input_data.csv`. Test labels are intentionally excluded here and stored separately in `reference_data/` for secure evaluation.