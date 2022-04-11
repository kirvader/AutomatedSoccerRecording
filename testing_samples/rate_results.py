import os
import sys
import argparse
from functools import cmp_to_key
from pathlib import Path


PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)

sys.path.append(PROJECT_ROOT)


from temp_utils.custom_model_results_folder import get_custom_model_results_folder


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name")
    parser.add_argument("--eps", type=int, default=0.02, help="Accuracy of boxes equality.")

    return parser.parse_args()


class ClassifiedBox:
    def __init__(self, class_num, center_x, center_y, width, height):
        self.class_num = class_num
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

    def comparator(self, other):
        if self.class_num < other.class_num:
            return -1
        if self.class_num > other.class_num:
            return 1
        if self.center_x < other.center_x:
            return -1
        if self.center_x > other.center_x:
            return 1
        if self.center_y < other.center_y:
            return -1
        if self.center_y > other.center_y:
            return 1
        return 0


def boxes_are_almost_same(box1, box2, eps=0.02):
    if box1.class_num != box2.class_num:
        return False
    if abs(box1.center_x - box2.center_x) > eps:
        return False
    if abs(box1.center_y - box2.center_y) > eps:
        return False
    if abs(box1.width - box2.width) > eps:
        return False
    if abs(box1.height - box2.height) > eps:
        return False
    return True


def get_results(str_path):
    if not Path(str_path).exists():
        return []
    result = []
    with open(str_path) as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split(' ')
            result.append(ClassifiedBox(int(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3]), float(tokens[4])))
    result = sorted(result, key=cmp_to_key(ClassifiedBox.comparator))
    return result


args = parse_args()
model = args.model
eps = args.eps

entered_model_results_folder = Path(PROJECT_ROOT) / Path(f"{get_custom_model_results_folder(model)}/labels/")
processed_images_folder = Path(PROJECT_ROOT) / Path('testing_samples/images/')
real_results_folder = Path(PROJECT_ROOT) / Path('testing_samples/labels/')

count_of_accepted = 0
count_of_all_images = 0

for img_path in processed_images_folder.glob('*.jpg'):
    count_of_all_images += 1
    img_name = str(img_path.name)[:-4]
    real_result = get_results(str(real_results_folder / Path(f"{img_name}.txt")))
    entered_model_result = get_results(str(entered_model_results_folder / Path(f"{img_name}.txt")))
    if len(real_result) != len(entered_model_result):
        continue
    if all(boxes_are_almost_same(real_result[i], entered_model_result[i], eps) for i in range(len(real_result))):
        count_of_accepted += 1

print(count_of_accepted / count_of_all_images)
