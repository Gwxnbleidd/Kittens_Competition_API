import sys
import os

cur_file_path = os.path.abspath(__file__)
tests_file_path = os.path.dirname(cur_file_path)
project_dir_path = os.path.dirname(tests_file_path)
sys.path.append(project_dir_path)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import TEST_DB_URL
from app.database.engine import Base, get_session

from main import app

client = TestClient(app)

test_engine = create_engine(url=TEST_DB_URL, echo=False)

test_session_factory = sessionmaker(test_engine)


def get_test_session():
    with test_session_factory() as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(autouse=True, scope='session')
def prepare_database():
    with test_engine.begin() as conn:
        Base.metadata.create_all(conn)
    yield
    with test_engine.begin() as conn:
        Base.metadata.drop_all(conn)
