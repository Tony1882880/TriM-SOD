# dataset settings
dataset_type = 'MMSODataset'  # 数据集类型，这将被用来定义数据集
data_root = '../out/cut_result'  # 数据的根路径
crop_size = (512, 512)  # 训练时的裁剪大小

test_pipeline = [
    dict(type='LoadImageFromFile'),  # 第1个流程，从文件路径里加载图像
    dict(type='PackSegInputs')  # 打包用于语义分割的输入数据
]

val_dataloader = dict(
    batch_size=1,  # 每一个GPU的batch size大小
    num_workers=4,  # 为每一个GPU预读取数据的进程个数
    persistent_workers=True,  # 在一个epoch结束后关闭worker进程，可以加快训练速度
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(  # 测试数据集配置
        type=dataset_type,  # 数据集类型，详见mmseg/datasets/
        data_root=data_root,  # 数据集的根目录
        pipeline=test_pipeline))  # 数据处理流程，它通过之前创建的test_pipeline传递。
test_dataloader = val_dataloader
test_evaluator = val_evaluator