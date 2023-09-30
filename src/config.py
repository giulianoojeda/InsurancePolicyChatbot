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

os.environ['OPENAI_API_KEY'] = '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'
os.environ["SERPER_API_KEY"] = "601eb132875f9c48e2686ef59909aeb124c1f81d"
os.environ["AWS_ACCESS_KEY_ID"] = "AKIA2JHUK4EGBAMYAYFY"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
#os.environ["OPENAI_NAME"] = ""

# Define environment variables
AWS_ACCESS_KEY_ID = str(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))
SERPER_API_KEY = str(os.getenv("SERPER_API_KEY"))
#OPENAI_NAME = str(os.getenv("OPENAI_NAME"))
