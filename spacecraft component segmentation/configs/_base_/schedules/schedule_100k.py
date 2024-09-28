# optimizer
optimizer = dict(type='SGD', lr=0.012, momentum=0.9, weight_decay=0.0005)
optim_wrapper = dict(type='OptimWrapper', optimizer=optimizer, clip_grad=None)
# learning policy
param_scheduler = [
    dict(
        type='PolyLR',
        eta_min=1e-4,
        power=0.9,
        begin=0,
        end=100000,
        by_epoch=False)
]
# training schedule for 80k
train_cfg = dict(type='IterBasedTrainLoop', max_iters=100000, val_interval=4000)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=10, log_metric_by_epoch=True),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', save_best='mIoU', by_epoch=True, interval=1000),
    sampler_seed=dict(type='DistSamplerSeedHook'))
    # visualization=dict(type='SegVisualizationHook', draw=True, interval=100))
