_base_ = [
    './_base_/models/upernet_r50.py',
    './_base_/datasets/MMSO_512x512.py', './_base_/default_runtime.py',
    './_base_/schedules/schedule_240k.py'
]
crop_size = (512, 512)
data_preprocessor = dict(size=crop_size)
model = dict(
    data_preprocessor=data_preprocessor,
    decode_head=dict(align_corners=True, num_classes=7),
    auxiliary_head=dict(align_corners=True, num_classes=7),
    test_cfg=dict(mode='slide', crop_size=(512, 512), stride=(341, 341)))
