_base_ = './deeplabv3plus_r50-d8_1xb2-40k_MMSO-1024x1024.py'
model = dict(pretrained='open-mmlab://resnet101_v1c', backbone=dict(depth=101))
