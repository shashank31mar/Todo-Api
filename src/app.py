from flask import Flask
from src.config import app_config
from src.db import db
from src.views.UserView import user_api as user_blueprint


def create_app(env_name):
	"""
		Create App
		:param env_name:
		:return:
		"""

	# APP initialization
	app = Flask(__name__)
	print(app_config[env_name])
	app.config.from_object(app_config[env_name])

	db.init_app(app)
	app.register_blueprint(user_blueprint)

	# endpoint for the base
	@app.route("/", methods=['GET'])
	def index():
		"""
		endpoint
		:return:
		"""
		return "Vola!!"

	return app


def create_test_app(env_name):
	"""
	Create App
	:param env_name:
	:return:
	"""

	# APP initialization
	app = Flask(__name__)
	print(app_config[env_name])
	app.config.from_object(app_config[env_name])

	db.init_app(app)
	app.register_blueprint(user_blueprint)

	# endpoint for the base
	@app.route("/", methods=['GET'])
	def index():
		"""
		endpoint
		:return:
		"""
		return "Vola test!!"

	return app, app_config[env_name].db_fd, app_config[env_name].SQLALCHEMY_DATABASE_URI
