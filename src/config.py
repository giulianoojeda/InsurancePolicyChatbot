from pathlib import Path
import os
from dotenv import load_dotenv

# Define paths
DATASET_ROOT_PATH = str(Path(__file__).parent.parent / "dataset")
ENV_PATH = str(Path(__file__).parent.parent / ".env")
CHROMA_PATH = str(Path(__file__).parent.parent / "chroma")

# Define Constants
S3_BUCKET_NAME = "anyoneai-datasets"
S3_BUCKET_PREFIX = "queplan_insurance/"

# Load .env file
load_dotenv(dotenv_path=ENV_PATH)

# Define environment variables
AWS_ACCESS_KEY_ID = str(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))
FAST_LLM_MODEL = str(os.getenv("FAST_LLM_MODEL"))
TEMPERATURE = float(os.getenv("TEMPERATURE"))
GOOGLE_API_KEY = str(os.getenv("GOOGLE_API_KEY"))
CUSTOM_SEARCH_ENGINE_ID = str(os.getenv("CUSTOM_SEARCH_ENGINE_ID"))
