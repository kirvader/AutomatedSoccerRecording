import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_video_path", help="Path to the video you want to slice for pieces")
parser.add_argument("--frame_rate", type=int, default=30, help="Every frame which order number can be divided by "
                                                               "frame_rate will be saved.")
parser.add_argument("--output_frames_folder_path", default="output/frames/", help="Path for the place you want"
                                                                                  " frames to be stored.")

args = parser.parse_args()

cap = cv2.VideoCapture(args.input_video_path)
success, img = cap.read()
frame_number = 0


def save_img(folder, index, img):
    cv2.imwrite(f"{folder}frame{index}.jpg", img)


while success:
    frame_number += 1

    if frame_number % args.frame_rate == 0 and success:
        save_img(args.output_frames_folder_path, frame_number // args.frame_rate, img)
    success, img = cap.read()

    if frame_number % (100 * args.frame_rate) == 0:
        print(f"{frame_number // args.frame_rate} frames stored!")


print(f"Finally all {frame_number // args.frame_rate} frames stored!")
