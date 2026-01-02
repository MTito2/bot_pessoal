import sys
from pathlib import Path
from openai import OpenAI

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(ROOT_DIR))

from keys import OPENAI_KEY




