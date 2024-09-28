# dataset settings
dataset_type = 'CocoDataset'
data_root = 'data/TriM-SOD/'

# Example to use different file client
# Method 1: simply set the data root and let the file I/O module
# automatically infer from prefix (not support LMDB and Memcache yet)

# data_root = 's3://openmmlab/datasets/detection/coco/'

# Method 2: Use `backend_args`, `file_client_args` in versions before 3.0.0rc6
# backend_args = dict(
#     backend='petrel',
#     path_mapping=dict({
#         './data/': 's3://openmmlab/datasets/detection/',
#         'data/': 's3://openmmlab/datasets/detection/'
#     }))
backend_args = None

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

train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=backend_args),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', scale=(512, 512), keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]
test_pipeline = [
    dict(type='LoadImageFromFile', backend_args=backend_args),
    dict(type='Resize', scale=(512, 512), keep_ratio=True),
    # If you don't have a gt annotation, delete the pipeline
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor'))
]
train_dataloader = dict(
    batch_size=8,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/train.json',
        data_prefix=dict(img='images/'),
        filter_cfg=dict(filter_empty_gt=True, min_size=32),
        pipeline=train_pipeline,
        backend_args=backend_args))
val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/val.json',
        data_prefix=dict(img='images/'),
        test_mode=True,
        pipeline=test_pipeline,
        backend_args=backend_args))
test_dataloader = val_dataloader

val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'annotations/val.json',
    metric='bbox',
    format_only=False,
    backend_args=backend_args)
test_evaluator = val_evaluator

# inference on test dataset and
# format the output results for submission.
# test_dataloader = dict(
#     batch_size=1,
#     num_workers=2,
#     persistent_workers=True,
#     drop_last=False,
#     sampler=dict(type='DefaultSampler', shuffle=False),
#     dataset=dict(
#         type=dataset_type,
#         data_root=data_root,
#         ann_file=data_root + 'annotations/image_info_test-dev2017.json',
#         data_prefix=dict(img='test2017/'),
#         test_mode=True,
#         pipeline=test_pipeline))
# test_evaluator = dict(
#     type='CocoMetric',
#     metric='bbox',
#     format_only=True,
#     ann_file=data_root + 'annotations/image_info_test-dev2017.json',
#     outfile_prefix='./work_dirs/coco_detection/test')
