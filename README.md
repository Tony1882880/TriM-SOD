# 🛰️ TriM-SOD: A Multi-modal, Multi-task, and Multi-scale Spacecraft Optical Dataset

> A public benchmark for space-based situational awareness (SSA) with visible-light and infrared imagery, multi-task labels, and broad target-size diversity.

---

## 📝 Abstract

The acquisition and application of spacecraft optical data is an important part of space-based situational awareness (SSA). Spacecraft optical data processing techniques can assist in tasks such as on-orbit operation, space debris removal, deep space exploration, \textit{etc}. However, the extreme lack of real spacecraft optical data is an insurmountable difficulty, which hinders the development of deep learning-based data processing techniques. Existing synthetic datasets usually only contain visible-light images, only support a specific task, and lack diversity in the scale of the spacecraft, which cannot adapt to actual application environments. Therefore, we propose a Multi-modal, Multi-task, and Multi-scale Spacecraft Optical Dataset (TriM-SOD), which has three superiorities: (a) Multi-modal: It includes data in various modals, such as visible-light and infrared; (b) Multi-task: It includes labels for multiple tasks, such as spacecraft detection and spacecraft component segmentation; (c) Multi-scale: It features a variety of sizes for spacecraft in the images. To validate the effectiveness of our dataset and evaluate the performance of methods in the tasks, we use TriM-SOD to train and test several typical or recent methods for object detection and semantic segmentation. TriM-SOD has been made public and can be used as a benchmark to further promote the future development of SSA.

---

## ✨ Highlights

- 🔭 **Multi-modal coverage:** **Visible-light** and **infrared** imagery; supports cross-modal training and evaluation.
- 🧩 **Multi-task supervision:** Annotations for **spacecraft detection** and **spacecraft component segmentation**.
- 📐 **Multi-scale targets:** Broad size distribution (small/medium/large).

---

## 🧪 Benchmark Code in This Repo

- This repository contains the **benchmark implementations** for **spacecraft detection** and **spacecraft component segmentation** on **TriM-SOD**.
- The codebase is **primarily adapted from [MMSegmentation](https://github.com/open-mmlab/mmsegmentation)** (data pipelines, configuration system, training/validation/evaluation utilities).  
  We added dataset adapters and task-specific components for TriM-SOD.
- Please keep the original attributions in the headers where present, and **comply with MMSegmentation’s license and usage terms** when using or redistributing derived code.

---

## 📦 Dataset Access (Kaggle)

The dataset is released in **PNG (uncompressed)** format and split into multiple parts on Kaggle:

- **Main package**  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-a-spacecraft-optical-dataset>

- **Supplementary packages** (mainly additional **visible-light** data)  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp1>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp2>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp3>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp4>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp5>

- **JPG Version (Compressed, The whole dataset)**  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-jpgversion>


---

## ⬇️ Quick Download (Kaggle CLI)

1) **Install & authenticate**

~~~bash
pip install kaggle
# Then place kaggle.json (Account → Create New API Token) at:
# Linux/Mac: ~/.kaggle/kaggle.json    Windows: %USERPROFILE%\.kaggle\kaggle.json
chmod 600 ~/.kaggle/kaggle.json  # Linux/Mac only
~~~

2) **Download all parts (to ./data)**

~~~bash
# Main
kaggle datasets download -d tonyyyyzhu/trim-sod-a-spacecraft-optical-dataset -p data/ --unzip

# Supplements (mostly visible-light additions)
kaggle datasets download -d tonyyyyzhu/trim-sod-supp1   -p data/ --unzip
kaggle datasets download -d tonyyyyzhu/trim-sod-supp2   -p data/ --unzip
kaggle datasets download -d tonyyyyzhu/trim-sod-supp3   -p data/ --unzip
kaggle datasets download -d tonyyyyzhu/trim-sod-supp4   -p data/ --unzip
kaggle datasets download -d tonyyyyzhu/trim-sod-supp5   -p data/ --unzip
~~~

---

## 🗂️ Folder Structure

> Place all six downloads under the same root so they merge into this structure:

```text
TriM-SOD/
├─ visible-light images/
├─ infrared images/
├─ component segmentation labels/
├─ detection labels/
├─ other labels/
├─ train.txt
└─ val.txt
```


---

## 📚 Citation

If you use **TriM-SOD** in your research, please cite the accompanying paper:

~~~bibtex
@article{TriM-SOD,
  title   = {TriM-SOD: A Multi-modal, Multi-task, and Multi-scale Spacecraft Optical Dataset},
  author  = {Zhu, Tianyu and Li, Hesong and Fu, Ying},
  journal = {Space: Science \& Technology},
  year    = {2025},
  publisher = {AAAS}
}
~~~

