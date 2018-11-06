import uuid
import datetime
from src.db import db
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
	# table name
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))
	password = db.Column(db.String(50))
	admin = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime)
	modified_at = db.Column(db.DateTime)

	# class constructor
	def __init__(self, data, admin):
		"""
		Class Constructor
		:param data:
		:param admin:
		"""
		self.name = data.get('name')
		self.public_id = str(uuid.uuid4())
		self.password = self.__generate_hash(data.get('password'))
		self.admin = admin
		self.created_at = datetime.datetime.utcnow()
		self.modified_at = datetime.datetime.utcnow()

	def save(self):
		"""
		Save data to db
		:return:
		"""
		db.session.add(self)
		db.session.commit()

	def delete(self):
		"""
		Delete data from db
		:return:
		"""
		db.session.delete(self)
		db.session.commit()

	# add this new method
	@staticmethod
	def __generate_hash(password):
		"""
		Generate Hash for password
		:param password:
		:return:
		"""
		return generate_password_hash(password, method='sha256')

	# add this new method
	def check_hash(self, password):
		"""
		Verify hash
		:param password:
		:return:
		"""
		return check_password_hash(self.password, password)

	@staticmethod
	def get_all_users():
		"""
		Get All users from DB
		:return:
		"""
		return User.query.all()

	@staticmethod
	def get_users_list(users):
		"""
		Get users as list of dictionary
		:param users:
		:return:
		"""
		output = []
		for user in users:
			output.append(User.get_user_dic(user))
		return jsonify({'users': output})

	@staticmethod
	def get_user_dic(user):
		"""
		Convert User object to dictionary
		:param user:
		:return:
		"""
		user_data = {}
		user_data['public_id'] = user.public_id
		user_data['name'] = user.name
		user_data['password'] = user.password
		user_data['created_at'] = user.created_at
		user_data['modified_at'] = user.modified_at
		user_data['admin'] = user.admin
		return user_data

	@staticmethod
	def get_one_user(public_id):
		"""
		Get used by Id
		:param public_id:
		:return:
		"""
		user = User.query.filter_by(public_id=public_id).first()
		if not user:
			return jsonify({'message': 'no user found!'})
		return jsonify({'user': User.get_user_dic(user)})

	@staticmethod
	def get_user_by_name(username):
		"""
		Get user by name
		:param username:
		:return:
		"""
		return User.query.filter_by(name=username).first()

	@staticmethod
	def promote_user(public_id):
		"""
		Promote User to Admin Status
		:param public_id:
		:return:
		"""
		user = User.query.filter_by(public_id=public_id).first()
		if not user:
			return jsonify({'message': 'no user found!'})
		user.admin = True
		user.save()
		return jsonify({'message': 'User has been promoted!'})

	@staticmethod
	def delete_user(public_id):
		"""
		Delete user with given id
		:param public_id:
		:return:
		"""
		user = User.query.filter_by(public_id=public_id).first()
		if not user:
			return jsonify({'message': 'no user found!'})

		user.delete()
		return jsonify({'message': 'User has been deleted!'})

	def __repr__(self):
		return '<id {}>'.format(self.id)
