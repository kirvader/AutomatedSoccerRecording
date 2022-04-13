import argparse
from temp_utils.model_processor import process_source_with_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("type_of_images_set", type=str, default=None,
                        help="train/val/test. Will use images from dataset/images/<your choice>")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_source_with_model(
        source=f"dataset/images/{args.type_of_images_set}",
        project_path="dataset",
        name=args.type_of_images_set,
        model="yolov5x6.pt"
    )
