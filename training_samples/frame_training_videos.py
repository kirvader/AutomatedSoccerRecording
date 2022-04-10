import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from pathlib import Path
from temp_utils.VideoSlicer.getting_images_from_video import slice_video_for_frames

paths_list = Path(str(PROJECT_ROOT / Path('training_samples/videos/'))).glob('*.mp4')
for path in paths_list:
    print(f"Starting slicing of {str(path)} video:")
    slice_video_for_frames(input_video_path=str(path),
                           output_frames_folder_path=str(PROJECT_ROOT / Path('training_samples/images/')))
