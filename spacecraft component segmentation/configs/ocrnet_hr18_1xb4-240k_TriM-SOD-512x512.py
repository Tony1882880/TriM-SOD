_base_ = [
    './_base_/models/ocrnet_hr18.py', './_base_/datasets/MMSO_512x512.py',
    './_base_/default_runtime.py', './_base_/schedules/schedule_240k.py'
]
crop_size = (512, 512)
data_preprocessor = dict(size=crop_size)
model = dict(data_preprocessor=data_preprocessor)
