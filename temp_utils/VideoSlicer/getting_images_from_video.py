import os
from pathlib import Path

import cv2
import argparse


def parse_args_for_one_video():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_video_path", help="Path to the video you want to slice for pieces")
    parser.add_argument("--frame_rate", type=int, default=30, help="Every frame which order number can be divided by "
                                                                   "frame_rate will be saved.")
    parser.add_argument("--output_frames_folder_path", default="output/frames/", help="Path for the place you want"
                                                                                      " frames to be stored.")

    return parser.parse_args()


def slice_video_for_frames(input_video_path, frame_rate=30, output_frames_folder_path="output/frames/"):
    cap = cv2.VideoCapture(input_video_path)
    success, img = cap.read()
    frame_number = 0

    def get_name_from_path(path):
        return Path(path).name.split('.')[0]

    def save_img(folder, name, index, img):
        os.makedirs(folder, exist_ok=True)
        path = Path(f"{folder}/{name}_{index}.jpg")

        if not cv2.imwrite(str(path.absolute()), img):
            raise Exception("Bad path")

    print(get_name_from_path(input_video_path))

    while success:
        frame_number += 1

        if frame_number % frame_rate == 0 and success:
            save_img(output_frames_folder_path, get_name_from_path(input_video_path), frame_number // frame_rate, img)
        success, img = cap.read()

        # if frame_number % (100 * frame_rate) == 0:
        #     print(f"{frame_number // frame_rate} frames stored!")

    print(f"Finally all {frame_number // frame_rate} frames stored!")
    return frame_number // frame_rate


if __name__ == "__main__":
    args = parse_args_for_one_video()
    slice_video_for_frames(input_video_path=args.input_video_path,
                           frame_rate=args.frame_rate,
                           output_frames_folder_path=args.output_frames_folder_path)
