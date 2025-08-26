# TriM-SOD: A Multi-modal, Multi-task, and Multi-scale Spacecraft Optical Dataset

> A public benchmark for space-based situational awareness (SSA) with visible-light and infrared imagery, multi-task labels, and broad target-size diversity.

---

## Abstract

The acquisition and application of spacecraft optical data is an important part of space-based situational awareness (SSA). Spacecraft optical data processing techniques can assist in tasks such as on-orbit operation, space debris removal, deep space exploration, \textit{etc}. However, the extreme lack of real spacecraft optical data is an insurmountable difficulty, which hinders the development of deep learning-based data processing techniques. Existing synthetic datasets usually only contain visible-light images, only support a specific task, and lack diversity in the scale of the spacecraft, which cannot adapt to actual application environments. Therefore, we propose a Multi-modal, Multi-task, and Multi-scale Spacecraft Optical Dataset (TriM-SOD), which has three superiorities: (a) Multi-modal: It includes data in various modals, such as visible-light and infrared; (b) Multi-task: It includes labels for multiple tasks, such as spacecraft detection and spacecraft component segmentation; (c) Multi-scale: It features a variety of sizes for spacecraft in the images. To validate the effectiveness of our dataset and evaluate the performance of methods in the tasks, we use TriM-SOD to train and test several typical or recent methods for object detection and semantic segmentation. TriM-SOD has been made public and can be used as a benchmark to further promote the future development of SSA.

---

## Highlights

- **Multi-modal coverage:** Visible-light **and** infrared imagery; supports cross-modal training and evaluation.
- **Multi-task supervision:** Unified annotations for **spacecraft detection** and **component-level semantic segmentation**.
- **Multi-scale targets:** Broad size distribution (small/medium/large) to stress-test scale robustness and long-range perception.
- **Benchmark-ready:** Public release with **official splits** (`train.txt`, `val.txt`) to ensure reproducible comparisons.
- **Practical organization:** Straightforward folder layout; compatible with common detection/segmentation toolchains.

---

## Dataset Access (Kaggle)

The dataset is large and released as **six parts** on Kaggle:

- **Main package**  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-a-spacecraft-optical-dataset>

- **Supplementary packages** (mainly additional **visible-light** data)  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp1>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp-2>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp3>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp4>  
  - 🔗 <https://www.kaggle.com/datasets/tonyyyyzhu/trim-sod-supp5>

> **Note:** Download **all six** parts and extract them into the **same root directory** so their contents are merged.

---

## Quick Download (Kaggle CLI)

1) **Install & authenticate**
```bash
pip install kaggle
# Then place kaggle.json (Account → Create New API Token) at:
# Linux/Mac: ~/.kaggle/kaggle.json    Windows: %USERPROFILE%\.kaggle\kaggle.json
chmod 600 ~/.kaggle/kaggle.json  # Linux/Mac only


### Citation

If you use TriM‑SOD in your research, please cite the accompanying
paper:

```
@article{TriM-SOD,
  title={TriM‑SOD: A Multi‑modal, Multi‑task, and Multi‑scale Spacecraft Optical Dataset},
  author={Zhu, Tianyu and Li, Hesong and Fu, Ying},
  journal={Space: Science \& Technology},
  year={2025},
  publisher={AAAS}
}
```

TriM‑SOD is released under the MIT License (see `LICENSE`).
