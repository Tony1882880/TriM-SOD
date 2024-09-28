_base_ = [
    '../_base_/models/ssd300.py', '../_base_/datasets/TriM-SOD_detection.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]

class_name = ('AcrimSAT', 'AIM', 'Aqua', 'Aquarius', 'Aura', 'Cassini', 'Chandra',
              'Clementine', 'CloudSAT', 'CNOFS', 'Dawn', 'Deepimpact', 'Deepspace', 'IceCube',
              'IceSat', 'Juno', 'Kepler', 'LandSAT', 'LRO', 'Magellan', 'Maven',
              'Messenger', 'MGS', 'MRO', 'Near', 'Npp', 'OSTM', 'Pioneer',
              'Rosetta', 'SACC', 'SOHO', 'SpaceX', 'TDRS', 'Ulysses', 'Voyager')
num_classes = len(class_name)

# palette参数里面的元组，有多少种类就有多少个元组(r,g,b)，否则报错
metainfo = dict(
    classes=class_name,
    palette=[(190, 201, 190), (135, 221, 87), (24, 82, 17), (160, 246, 172), (167, 65, 254), (53, 230, 101),
             (83, 194, 98), (79, 32, 224), (134, 105, 71), (89, 170, 245), (185, 100, 122), (147, 0, 142),
             (54, 79, 14), (178, 254, 201), (59, 84, 220), (233, 18, 34), (243, 1, 246), (15, 12, 224),
             (19, 69, 219), (35, 63, 230), (110, 55, 91), (92, 179, 233), (198, 82, 243), (65, 235, 90),
             (105, 46, 48), (189, 113, 83), (64, 30, 154), (106, 51, 48), (49, 21, 32), (121, 62, 91),
             (177, 136, 208), (71, 139, 21), (155, 11, 227), (112, 244, 104), (225, 211, 150)]  # 画图时候的颜色，随便设置即可
)

# dataset settings
input_size = 300
train_pipeline = [
    dict(type='LoadImageFromFile', backend_args={{_base_.backend_args}}),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='Expand',
        mean={{_base_.model.data_preprocessor.mean}},
        to_rgb={{_base_.model.data_preprocessor.bgr_to_rgb}},
        ratio_range=(1, 4)),
    dict(
        type='MinIoURandomCrop',
        min_ious=(0.1, 0.3, 0.5, 0.7, 0.9),
        min_crop_size=0.3),
    dict(type='Resize', scale=(input_size, input_size), keep_ratio=False),
    dict(type='RandomFlip', prob=0.5),
    dict(
        type='PhotoMetricDistortion',
        brightness_delta=32,
        contrast_range=(0.5, 1.5),
        saturation_range=(0.5, 1.5),
        hue_delta=18),
    dict(type='PackDetInputs')
]
test_pipeline = [
    dict(type='LoadImageFromFile', backend_args={{_base_.backend_args}}),
    dict(type='Resize', scale=(input_size, input_size), keep_ratio=False),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor'))
]
train_dataloader = dict(
    batch_size=16,
    num_workers=8,
    batch_sampler=None,
    dataset=dict(
        _delete_=True,
        type='RepeatDataset',
        times=5,
        dataset=dict(
            type={{_base_.dataset_type}},
            data_root={{_base_.data_root}},
            metainfo=metainfo,
            ann_file='annotations/train.json',
            data_prefix=dict(img='images/'),
            filter_cfg=dict(filter_empty_gt=True, min_size=32),
            pipeline=train_pipeline,
            backend_args={{_base_.backend_args}})))
val_dataloader = dict(batch_size=1,
                      num_workers=2,
                      dataset=dict(pipeline=test_pipeline))
test_dataloader = val_dataloader

# optimizer
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(type='SGD', lr=2e-3, momentum=0.9, weight_decay=5e-4))

custom_hooks = [
    dict(type='NumClassCheckHook'),
    dict(type='CheckInvalidLossHook', interval=50, priority='VERY_LOW')
]

# NOTE: `auto_scale_lr` is for automatically scaling LR,
# USER SHOULD NOT CHANGE ITS VALUES.
# base_batch_size = (8 GPUs) x (8 samples per GPU)
auto_scale_lr = dict(base_batch_size=16)
