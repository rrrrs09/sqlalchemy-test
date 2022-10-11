import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DSN: str = os.environ["POSTGRES_DSN"]
NODES_PER_LEVEL: int = int(os.getenv("NODES_PER_LEVEL", 5))
MAX_DEPTH: int = int(os.getenv("MAX_DEPTH", 4))
