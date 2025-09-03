# IVPR Lab 4 – Frequency Domain Image Processing

## 📌 Overview
This lab demonstrates various **frequency domain techniques** in image processing using Python, OpenCV, NumPy, and Matplotlib. The focus is on applying **Fourier Transform–based filters**, creating **hybrid images**, and **denoising images** via frequency spectrum manipulation.  

The experiments are interactive (with `ipywidgets`) and provide visualizations of the **DFT spectrum**, **filter masks**, and the **final processed images**.

---

## 📂 Experiments

### 🔹 Q1: Frequency Domain Filtering
- Implemented **Low-Pass** and **High-Pass** filters:
  - Ideal Filter
  - Gaussian Filter
  - Butterworth Filter
- Used **Discrete Fourier Transform (DFT)** and **Inverse DFT**.
- Interactive visualization with sliders for cutoff frequency.
- Outputs:
  - DFT Spectrum
  - Filter Mask
  - Filtered Image

---

### 🔹 Q2: Hybrid Images
- Created **hybrid images** by combining:
  - **High-pass filtered image** (Einstein)
  - **Low-pass filtered image** (Marilyn)
- Controlled with parameters:
  - Cutoff frequency (high & low)
  - Filter type (Gaussian / Butterworth)
  - Alpha & Beta blending factors
- Output:
  - Hybrid image that changes perception with viewing distance.

---

### 🔹 Q3: Noise Removal in Frequency Domain
- Processed noisy images of **Cameraman**.
- Applied **FFT spectrum editing** to remove periodic noise.
- Steps:
  - Identify and suppress noise frequencies in Fourier domain.
  - Perform **Inverse FFT** to reconstruct denoised image.
- Outputs:
  - Noisy Image
  - Original Magnitude Spectrum
  - Cleaned Spectrum
  - Restored Image

---

## 🛠️ Requirements
Install dependencies before running:

```bash
pip install numpy opencv-python matplotlib ipywidgets
```

---

## ▶️ Usage
Run the notebook in **Google Colab** or Jupyter:

```bash
jupyter notebook IVPR_LAB_4.ipynb
```

- For Q1, interact with filter type and cutoff frequency.
- For Q2, experiment with hybrid image parameters.
- For Q3, run the denoising function on noisy images.

---

## 📊 Results
- Demonstrated **frequency domain filtering** for image enhancement.
- Generated **hybrid images** showcasing spatial-frequency perception.
- Successfully **removed periodic noise** from images using FFT.
