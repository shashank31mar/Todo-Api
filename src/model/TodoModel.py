from src.db import db
import datetime
from flask import jsonify


class Todo(db.Model):
	# table name
	__tablename__ = 'todo'

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(50))
	complete = db.Column(db.Boolean)
	user_id = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	modified_at = db.Column(db.DateTime)

	# class constructor
	def __init__(self, text, complete, user_id):
		"""
		Class Constructor
		:param text:
		:param complete:
		:param user_id:
		"""
		self.text = text
		self.user_id = user_id
		self.complete = complete
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

	@staticmethod
	def get_todos_for_user(user_id):
		"""
		Get todo list for a user
		:param user_id:
		:return:
		"""
		todos = Todo.query.filter_by(user_id=user_id).all()
		output = []

		for todo in todos:
			todo_data = {}
			todo_data['id'] = todo.id
			todo_data['text'] = todo.text
			todo_data['complete'] = todo.complete
			output.append(todo_data)

		return jsonify({'todos': output})

	@staticmethod
	def get_one_todo_for_user(user_id, todo_id):
		"""
		Get a specific tod item for a user
		:param user_id:
		:param todo_id:
		:return:
		"""
		todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
		if not todo:
			return jsonify({'message': 'No todo found!'})
		return jsonify(Todo.get_todo_dic(todo))

	@staticmethod
	def get_todo_dic(todo):
		"""
		Convert todo object to dictionary
		:param todo:
		:return:
		"""
		todo_data = {}
		todo_data['id'] = todo.id
		todo_data['text'] = todo.text
		todo_data['complete'] = todo.complete
		return todo_data

	@staticmethod
	def complete_todo(user_id, todo_id):
		"""
		Complete a todo item for a user
		:param user_id:
		:param todo_id:
		:return:
		"""
		todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
		if not todo:
			return jsonify({'message': 'No todo found!'})
		todo.complete = True
		todo.save()
		return jsonify({'message': 'Todo item has been completed!'})

	@staticmethod
	def delete_todo(user_id, todo_id):
		"""
		Delete a todo item for a user
		:param user_id:
		:param todo_id:
		:return:
		"""
		todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
		if not todo:
			return jsonify({'message': 'No todo found!'})
		todo.delete()
		return jsonify({'message': 'Todo item deleted!'})

	@staticmethod
	def update_todo(user_id, todo_id, text):
		"""
		Update the content to todo item for a user
		:param user_id:
		:param todo_id:
		:param text:
		:return:
		"""
		todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
		if not todo:
			return jsonify({'message': 'No todo found!'})
		todo.text = text
		todo.save()
		return jsonify({'message': 'Todo item has been updated!'})
