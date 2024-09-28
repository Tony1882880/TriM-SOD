_base_ = [
    '../_base_/models/faster-rcnn_r50_fpn.py',
    '../_base_/datasets/TriM-SOD_detection.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]

load_from = "https://download.openxlab.org.cn/models/mmdetection/FasterR-CNN/weight/faster-rcnn_r50_fpn_1x_coco"

class_name = ('AcrimSAT', 'AIM', 'Aqua', 'Aquarius', 'Aura', 'Cassini', 'Chandra',
              'Clementine', 'CloudSAT', 'CNOFS', 'Dawn', 'Deepimpact', 'Deepspace', 'IceCube',
              'IceSat', 'Juno', 'Kepler', 'LandSAT', 'LRO', 'Magellan', 'Maven',
              'Messenger', 'MGS', 'MRO', 'Near', 'Npp', 'OSTM', 'Pioneer',
              'Rosetta', 'SACC', 'SOHO', 'SpaceX', 'TDRS', 'Ulysses', 'Voyager')
num_classes = len(class_name)

model = dict(
    roi_head=dict(
        bbox_head=dict(
            num_classes=num_classes
        )
    )
)

default_hooks = dict(
    checkpoint=dict(
        interval=1,
        max_keep_ckpts=2,  # only keep latest 3 checkpoints
        save_best='auto'
    ))

train_cfg = dict(max_epochs=50, val_interval=10)

param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=1000),
    dict(
        type='MultiStepLR',
        begin=0,
        end=50,
        by_epoch=True,
        milestones=[34, 42],
        gamma=0.1)
]