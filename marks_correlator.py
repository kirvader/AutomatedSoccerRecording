import argparse
from pathlib import Path

names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']

filtered_labels = ['person', 'bench', 'backpack', 'handbag', 'suitcase', 'sports ball', 'bottle', 'chair', 'couch',
                   'potted plant', 'tv', 'clock', 'dining table']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default=None,
                        help="None/train/val/test. Will correlate all markers from dataset/<type>/labels and write to dataset/labels/test")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    all_dirs = [args.type]
    if args.type is None:
        all_dirs = ['train', 'test', 'val']
    for label in all_dirs:
        folder_to_read_from = Path(f"dataset/{label}/labels/")
        for path in folder_to_read_from.glob('*.txt'):
            filename = path.name
            with open(path, 'r') as r:
                lines = r.readlines()
                with open(f"dataset/labels/{label}/{filename}", "w") as w:
                    for line in lines:
                        class_type = names[int(line.split(' ')[0])]
                        if class_type in filtered_labels:
                            w.write(line)
