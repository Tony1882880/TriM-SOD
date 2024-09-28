from mmseg.registry import DATASETS
from .basesegdataset import BaseSegDataset


@DATASETS.register_module()
class MMSODataset(BaseSegDataset):
    METAINFO = dict(
        classes=('background', 'antenna', 'body', 'panel',
                 'instrument', 'support', 'thrust'),
        palette=[[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255],
                 [255, 255, 0], [255, 0, 255], [0, 255, 255]]
    )

    def __init__(self, **kwargs):
        super(MMSODataset, self).__init__(
            img_suffix='.jpg',
            seg_map_suffix='.png',
            reduce_zero_label=False,
            **kwargs
        )
