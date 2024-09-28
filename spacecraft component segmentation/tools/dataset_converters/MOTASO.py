import os
import shutil
import cv2
import numpy as np

# 定义文件路径
src_image_dir = 'F:/Dataset/Spacecraft/TriM-SOD/visible-aftercutting'  # 图像源目录
src_label_dir = 'F:/Dataset/Spacecraft/TriM-SOD/segmentation-aftercutting'  # 标签源目录
dest_dir = 'E:/Task/Satellite Dataset/openmmlab/mmsegmentation/data/MMSO'  # 目标目录


# 定义函数来从给定的txt文件读取文件名列表
def read_list_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        new_lines = []
        for line in lines:
            new_lines.append(line.split('/')[-1].split('.')[0])
        print(new_lines)
        return new_lines


# 读取训练集和测试集列表
train_list = read_list_from_file(
    'E:/Task/Satellite Dataset/openmmlab/mmdetection/data/MOTASO/train.txt')  # 在此输入你的训练集txt文件路径
val_list = read_list_from_file(
    'E:/Task/Satellite Dataset/openmmlab/mmdetection/data/MOTASO/val.txt')  # 在此输入你的测试集txt文件路径


# 定义图像处理函数
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


# 定义路径拷贝函数
def copy_files(file_list, source_dir, dest_dir, is_img=True):
    for file in file_list:
        print(os.path.join(source_dir, file + '.png'))
        if os.path.exists(os.path.join(source_dir, file + '.png')):
            if is_img:
                shutil.copy(os.path.join(source_dir, file + '.png'), dest_dir)
            else:
                label_img_path = os.path.join(source_dir, file + '.png')
                processed_label_img = label_preprocessing(label_img_path)
                cv2.imwrite(os.path.join(dest_dir, file + '.png'), processed_label_img)


# 创建目录结构
os.makedirs(os.path.join(dest_dir, 'annotation', 'train'), exist_ok=True)
os.makedirs(os.path.join(dest_dir, 'annotation', 'val'), exist_ok=True)
os.makedirs(os.path.join(dest_dir, 'image', 'train'), exist_ok=True)
os.makedirs(os.path.join(dest_dir, 'image', 'val'), exist_ok=True)

# 拷贝文件
copy_files(train_list, src_image_dir, os.path.join(dest_dir, 'image', 'train'))
copy_files(val_list, src_image_dir, os.path.join(dest_dir, 'image', 'val'))
copy_files(train_list, src_label_dir, os.path.join(dest_dir, 'annotation', 'train'), is_img=False)
copy_files(val_list, src_label_dir, os.path.join(dest_dir, 'annotation', 'val'), is_img=False)
