# Overview of the Challenge

## Introduction
Accurate classification of grain varieties is a key challenge in modern agriculture, directly impacting crop evaluation, yield estimation, and harvest quality management. In many farming practices, multiple seed varieties are sown together in controlled proportions (for example, 50% of variety V1 and 50% of variety V2). However, after harvest, the actual yield distribution often differs from the initial seeding ratio due to factors such as growth performance, environmental adaptation, disease resistance, and inter-varietal interactions.

To assess these outcomes, it is necessary to identify and distinguish grain varieties after harvest. Hyperspectral imaging offers a powerful solution by capturing fine-grained spectral information across hundreds of wavelengths, revealing subtle differences that are invisible to standard RGB imaging. However, hyperspectral data is inherently high-dimensional and complex, requiring robust preprocessing, dimensionality reduction, and classification pipelines.

This challenge leverages real-world hyperspectral grain data provided by INRAE, collected across two consecutive crop years. Participants are invited to design and evaluate machine learning and deep learning models for fine-grained image classification, while also addressing key challenges such as class imbalance, domain shift across years, and generalization to unseen conditions.

---

## Competition Tasks
Participants are required to develop models that classify individual grain images into 8 distinct grain varieties.

### Primary Task
- **Multi-class image classification**: Predict the correct grain variety for each input grain image.

### Secondary Objectives
- **Robustness across crop years**: Models should generalize well across data collected in different years.
- **Handling class imbalance**: Some varieties may be under-represented, requiring careful training strategies.
- **Efficient feature learning**: Extract discriminative representations from reduced hyperspectral data.

---

## Dataset Description

### Raw Data Source
- Provider: **INRAE (French National Research Institute for Agriculture, Food and Environment)**
- Imaging modality: **Hyperspectral imaging**
- Number of spectral channels: **216**
- Crop years: **2019–2020**
- Original image shape: **(2048, 9100, 216)**
- Several hyperspectral images per variety and per year

### Preprocessing Pipeline
1. **Grain Segmentation**  
   A watershed-based segmentation algorithm is applied to the raw hyperspectral images to isolate individual grains, resulting in approximately **27,000 extracted grains**.

2. **Grain Cropping**  
   Each segmented grain is cropped into a patch of approximate size **252 × 252 × 216**.

3. **Dimensionality Reduction**  
   To reduce computational complexity, hyperspectral cubes are projected into three channels using either:
   - Principal Component Analysis (PCA), or
   - Selected RGB-equivalent spectral bands.

4. **Final Input Format**  
   Each grain is provided as a **224 × 224 × 3 image**, suitable for standard convolutional neural networks.

### Labels
- **8 grain varieties**

### Final Dataset
- Individual grain images of shape **(224, 224, 3)**
- Balanced training and testing splits with attention to crop year separation

---

## Competition Phases

1. **Development Phase**  
   Participants explore the dataset, build baseline models, and refine their approaches using the provided training data.

2. **Validation Phase**  
   Submissions are evaluated on a hidden validation set to provide leaderboard feedback.

3. **Final Evaluation Phase**  
   The final ranking is determined using a withheld test set, potentially including domain shifts across crop years.

---

## Evaluation Metrics

- **Primary Metric:** Classification Accuracy
- **Secondary Metrics (optional):**
  - Macro-averaged F1-score
  - Balanced Accuracy

These metrics encourage robust performance across all varieties, including minority classes.

---

## How to Join This Competition

1. Login or create an account on **Codabench**: https://www.codabench.org/
2. Navigate to the competition page.
3. Go to the **Starting Kit** tab.
4. Download the **Dummy Sample Submission**.
5. Register in the competition.
6. Submit your results through the **My Submissions** tab.

---

## Submissions

This competition accepts **result-only submissions**.

Participants must:
- Follow the submission format described in the **Starting Kit**.
- Upload a prediction file containing the predicted class for each test image.

Limits on the number of daily submissions may apply.

---

## Timeline

- **Competition Launch:** TBD
- **Development Phase:** TBD
- **Final Submission Deadline:** TBD
- **Results Announcement:** TBD

---

## Credits

- Dataset provided by **INRAE**
- Challenge design and academic supervision by the teaching and research staff
- Platform hosting: **Codabench**

---

## Contact

For questions regarding the dataset, evaluation, or submission process, please contact:

- **Course staff / organizers:** TBD
- **Technical support:** Codabench platform help center