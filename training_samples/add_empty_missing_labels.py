import os
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)

images_folder = Path(PROJECT_ROOT) / Path('training_samples/images/')
results_folder = Path(PROJECT_ROOT) / Path('training_samples/labels/')


for img_path in images_folder.glob('*.jpg'):
    img_name = img_path.name[:-4]
    expected_file = results_folder / Path(f"{img_name}.txt")
    open(str(expected_file), 'a').close()
