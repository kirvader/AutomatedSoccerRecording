import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)

sys.path.append(PROJECT_ROOT)

from temp_utils.model_processor import process_source_with_model

process_source_with_model(source='training_samples/images/',
                          project_path='training_samples')
