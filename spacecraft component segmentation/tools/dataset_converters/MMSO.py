import glob
import random
import shutil
from pathlib import Path

import cv2
import numpy as np


def label_preprocessing(label_img_path):
    # 以rgb模式读取图片
    label_img = cv2.imread(label_img_path, cv2.IMREAD_COLOR)
    label_img = cv2.cvtColor(label_img, cv2.COLOR_BGR2RGB)

    # 创建一个空的单通道图像(与原图大小一致)用于存放处理后的图像
    new_label_img = np.zeros(label_img.shape[:2], dtype=np.uint8)

    # 对rgb颜色进行枚举，将不同颜色映射为不同的像素值
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    for i, color in enumerate(colors):
        new_label_img[(label_img == color).all(axis=2)] = i

    return new_label_img.astype(np.uint8)


def main(ratio=0.9, shuffle=True):
    root_dir = Path("F:/Dataset/Spacecraft/TriM-SOD")
    img_paths = glob.glob(str(root_dir / "visible" / "*.png"))
    tokens = []
    for img_path in img_paths:
        tokens.append(img_path.split("\\")[-1].split(".")[0])
    n_total = len(tokens)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], tokens
    if shuffle:
        random.shuffle(tokens)
    train_tokens = tokens[:offset]
    val_tokens = tokens[offset:]
    print(f"train length: {len(train_tokens)}")
    print(f"val length: {len(val_tokens)}")

    for train_token in train_tokens:
        shutil.copy(str(root_dir / "visible" / (train_token + ".png")),
                    "E:/Task/Satellite Dataset/openmmlab/mmsegmentation/data/MMSO/image/train/")
        label = label_preprocessing(str(root_dir / "segmentation_new" / (train_token + ".png")))
        cv2.imwrite("E:/Task/Satellite Dataset/openmmlab/mmsegmentation/data/MMSO/annotation/train/"
                    + (train_token + ".png"), label)

    for val_token in val_tokens:
        shutil.copy(str(root_dir / "visible" / (val_token + ".png")),
                    "E:/Task/Satellite Dataset/openmmlab/mmsegmentation/data/MMSO/image/val/")
        label = label_preprocessing(str(root_dir / "segmentation_new" / (val_token + ".png")))
        cv2.imwrite("E:/Task/Satellite Dataset/openmmlab/mmsegmentation/data/MMSO/annotation/val/"
                    + (val_token + ".png"), label)


if __name__ == '__main__':
    main()
