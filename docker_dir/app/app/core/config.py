import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
TEST_DB_URL = os.getenv("TEST_DB_URL")