import os
import sys
import argparse

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)

sys.path.append(PROJECT_ROOT)

from temp_utils.custom_model_results_folder import get_custom_model_results_folder

from temp_utils.model_processor import process_source_with_model


def parse_model():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Model name ")

    return parser.parse_args()

model = parse_model().model
process_source_with_model(source='dataset/images/test/',
                          project_path=get_custom_model_results_folder(model),
                          model=model)
