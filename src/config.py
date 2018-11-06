import os
import tempfile

class Development(object):
	"""
	Development environment configuration
	"""
	DEBUG = True
	TESTING = False
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'todo_dev.sqlite')
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(object):
	"""
	Production environment configurations
	"""
	DEBUG = False
	TESTING = False
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'todo_prod.sqlite')
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(object):
	"""
	Testing environment configuration
	"""
	DEBUG = True
	TESTING = True
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

	basedir = os.path.abspath(os.path.dirname(__file__))
	db_fd, SQLALCHEMY_DATABASE_URI = tempfile.mkstemp()
	SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
	'development': Development,
	'production': Production,
	'testing': Testing
}