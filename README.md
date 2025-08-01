## TriM-SOD: A Multi‑modal, Multi‑task and Multi‑scale Spacecraft Optical Dataset

TriM‑SOD is a large benchmark designed to advance computer vision research for
spacecraft observation and situational awareness.  The dataset brings
together multi‑modal imagery, annotations for multiple tasks and samples
captured at different spatial resolutions.  Researchers can use TriM‑SOD to
train and evaluate algorithms for object detection, semantic segmentation,
component segmentation and classification across a wide range of spacecraft
types and imaging conditions.

### Key features

* **Multi‑modal data** – each observation includes both visible–light and
  infrared imagery.  Visible images come from optical sensors on board a
  variety of space‑borne platforms, while the infrared modality captures
  thermal emissions.  These complementary signals help algorithms cope with
  low‑light conditions, occlusions and varying spacecraft surface materials.
* **Multiple tasks** – TriM‑SOD contains annotations for object detection
  (bounding boxes around spacecraft and sub‑components) and detailed
  component segmentation masks.  A small set of high‑level class labels
  indicate the type of spacecraft (e.g. Earth observation satellite,
  planetary probe) for classification experiments.
* **Multi‑scale** – images were captured under different imaging distances and
  sensor resolutions.  Some examples show full spacecraft at far distances
  while others zoom in on individual components.  This diversity makes the
  dataset suitable for both small‑object and large‑object detection.
* **Large scale** – the first public release comprises approximately
  **209 GB** of data split into **438 k files**.  The training split
  (`train.txt`) lists several hundred thousand samples and the
  validation split (`val.txt`) contains held‑out examples for evaluation.

### Data organisation

The dataset is structured into several top‑level folders:

```
TriM‑SOD/
├── visible‑light images_1/    # optical RGB images
├── infrared images/           # thermal IR images
├── component segmentation/    # pixel‑wise masks for components
├── detection labels/          # bounding‑box annotations
├── other labels/              # additional metadata
├── train.txt                  # list of training sample identifiers
└── val.txt                    # list of validation sample identifiers
```

Each line in `train.txt` or `val.txt` refers to a particular
observation (for example, `Maven_camD17_79` or `Aquarius_camD13_76`).  The
prefix denotes the satellite or camera name (e.g., `Maven`, `Aquarius`,
`MRO`, `Magellan`), and the suffix is an internal identifier.  Use these
identifiers to locate the corresponding images and annotation files in the
respective directories.

### Downloading the data

Due to the large size of TriM‑SOD, the raw images and annotations are
hosted on Kaggle.  You **should not attempt to store the entire dataset
directly in this repository**.  Instead, follow the steps below to
download the data locally using the Kaggle API:

1. Install the Kaggle client:

   ```bash
   pip install kaggle
   ```

2. Generate an API token from your Kaggle account settings and place the
   downloaded `kaggle.json` in `~/.kaggle/` with permissions set to
   `600`.

3. Run the following command from the root of this repository to
   download and extract the dataset:

   ```bash
   kaggle datasets download -d tonyyyyzhu/trim-sod-a-spacecraft-optical-dataset -p data --unzip
   ```

   This will create a `data/` directory containing all images and labels.

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