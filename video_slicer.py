import argparse
from pathlib import Path

from temp_utils.VideoSlicer.getting_images_from_video import slice_video_for_frames


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_videos_folder", type=str, default=None,
                        help="Path to the video you want to slice for pieces(relative to project root)")
    parser.add_argument("--frame_rate", type=int, default=30, help="Every frame which order number can be divided by "
                                                                   "frame_rate will be saved.")
    parser.add_argument("--output_frames_folder", type=str, default="output/frames/", help="Path for the place you want"
                                                                                           " frames to be stored.(relative to project root)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    paths_list = Path(args.input_videos_folder).glob('*.mp4')
    for path in paths_list:
        print(f"Starting slicing of {str(path)} video:")
        slice_video_for_frames(input_video_path=str(path),
                               output_frames_folder_path=str(Path(args.output_frames_folder)))
