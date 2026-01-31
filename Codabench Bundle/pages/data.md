# Data Description

This page explains where the data comes from, how it was prepared, and what participants receive for the challenge. The goal is to make the dataset easy to understand and easy to use.

---

## Where Does the Data Come From?

The data is provided by **INRAE** (French National Research Institute for Agriculture, Food and Environment).

It comes from real experiments where harvested grains were scanned using **hyperspectral cameras**. These cameras capture much more information than normal RGB images by recording many wavelengths of light.

* **Crop years:** 2020
* **Context:** Post-harvest grain analysis
* **Goal:** Identify grain varieties after harvest to study yearly yield composition and performance

---

## Raw Hyperspectral Images (Not Provided)

Originally, the data consists of very large hyperspectral images:

* **Image size:** 2048 × 9100 pixels
* **Spectral channels:** 216 per pixel
* **Shape:** (2048, 9100, 216)

Each image contains many grains at once. These raw images are **not given to participants** because they are very large and difficult to process.

---

## Grain Extraction

To build the dataset:

* A **watershed segmentation algorithm** was used to automatically detect and separate individual grains from the background.
* **More than 10,000 individual grains** were extracted from all images and both years.

Each grain is then treated as a separate data sample.

---

## Grain Images Before Reduction

After segmentation:

* Each grain is cropped into a small hyperspectral cube of about:

  * **252 × 252 pixels**
  * **216 spectral channels**

This still represents a large amount of data per grain.

---

## Reducing the Number of Channels

Hyperspectral images have many channels, which makes them hard to use directly with standard machine learning models.

To simplify the data, each grain was converted to a **3‑channel image** using **RGB-like band selection:**

  * The images are now similar to what the human eye can see.
This step keeps most of the useful information while making the data much easier to handle.

---

## Final Dataset Provided to Participants

What you actually receive for the challenge:

* **Image size:** 224 × 224 × 3
* **One image = one grain**
* **Number of classes:** 8 grain varieties
* **Labels:** One label per image indicating the grain variety

---

## How to access the dataset

The dataset needed is provided in the **starter_kit.zip** file in the **Files** tab.

---

## Important Notes

* Raw hyperspectral images are not shared.
* All images are already segmented and preprocessed.
* Small visual artifacts may exist due to automatic processing.

Despite this, the dataset contains enough information to successfully distinguish grain varieties.
