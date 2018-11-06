import os
import pytest
from src.app import create_test_app


# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def client():
	"""
	Get Client
	:return:
	"""
	app, db_fd, db_uri = create_test_app('testing')
	client = app.test_client()

	yield client

	os.close(db_fd)
	os.unlink(db_uri)