from flask import request, jsonify, make_response, Blueprint, Response, json
from src.shared.Authentication import Auth
from src.model.UserModel import User
from src.model.TodoModel import Todo
user_api = Blueprint('users', __name__)


@user_api.route('/user', methods=['GET'])
@Auth.auth_required
def get_all_users(current_user):
	"""
	Get All users from Db
	:param current_user:
	:return:
	"""
	if not current_user.admin:
		return Response(
			mimetype="application/json",
			response=json.dumps({'error': 'cannot perform this action!'}),
			status=400
		)
	users = User.get_all_users()
	return User.get_users_list(users)


@user_api.route('/user/<public_id>', methods=['GET'])
@Auth.auth_required
def get_one_user(current_user, public_id):
	"""
	Get One user based on public_id
	:param current_user:
	:param public_id:
	:return:
	"""
	if not current_user.admin:
		return Response(
			mimetype="application/json",
			response=json.dumps({'error': 'cannot perform this action!'}),
			status=400
		)
	return User.get_one_user(public_id)


@user_api.route('/user/register', methods=['POST'])
@Auth.auth_required
def create_user(current_user):
	"""
	Create User
	:param current_user:
	:return:
	"""

	if not current_user.admin:
		return Response(
			mimetype="application/json",
			response=json.dumps({'error': 'cannot perform this action!'}),
			status=400
		)
	data = request.get_json()
	new_user = User(data, admin=False)
	new_user.save()

	return jsonify({'message': 'new user created!!'})


@user_api.route('/user/<public_id>', methods=['PUT'])
@Auth.auth_required
def promote_user(current_user, public_id):
	"""
	Promote User to Admin Status
	:param current_user:
	:param public_id:
	:return:
	"""
	if not current_user.admin:
		return Response(
			mimetype="application/json",
			response=json.dumps({'error': 'cannot perform this action!'}),
			status=400
		)
	return User.promote_user(public_id)


@user_api.route('/user/<public_id>', methods=['DELETE'])
@Auth.auth_required
def delete_user(current_user, public_id):
	"""
	Delete Specific user
	:param current_user:
	:param public_id:
	:return:
	"""
	if not current_user.admin:
		return Response(
			mimetype="application/json",
			response=json.dumps({'error': 'cannot perform this action!'}),
			status=400
		)
	return User.delete_user(public_id)


@user_api.route('/login', methods=['POST'])
def login():
	"""
	Authorize and create token for a session of a User
	:return:
	"""
	auth = request.get_json()
	#print("user name is : ".format(auth))
	if not auth or not auth['username'] or not auth['password']:
		return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

	user = User.get_user_by_name(auth['username'])

	if not user:
		return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

	if user.check_hash(auth['password']):
		return Auth.generate_token(user.public_id)

	return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@user_api.route('/todo', methods=['GET'])
@Auth.auth_required
def get_all_todos(current_user):
	"""
	Get All Todos for a specific user
	:param current_user:
	:return:
	"""
	return Todo.get_todos_for_user(current_user.id)


@user_api.route('/todo/<todo_id>', methods=['GET'])
@Auth.auth_required
def get_one_todo(current_user, todo_id):
	"""
	Get a specific Todo for a user
	:param current_user:
	:param todo_id:
	:return:
	"""
	return Todo.get_one_todo_for_user(current_user.id, todo_id)


@user_api.route('/todo', methods=['POST'])
@Auth.auth_required
def create_todo(current_user):
	"""
	Create Todo for a User
	:param current_user:
	:return:
	"""
	data = request.get_json()
	new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
	new_todo.save()

	return jsonify({'message': 'new todo created for user : ' + current_user.name})


@user_api.route('/todo/<todo_id>', methods=['PUT'])
@Auth.auth_required
def complete_todo(current_user, todo_id):
	"""
	Complete a specific todo for a user
	:param current_user:
	:param todo_id:
	:return:
	"""
	return Todo.complete_todo(current_user.id, todo_id)


@user_api.route('/todo/u', methods=['POST'])
@Auth.auth_required
def update_todo(current_user):
	data = request.get_json()
	return Todo.update_todo(current_user.id, data['todo_id'], data['text'])


@user_api.route('/todo/<todo_id>', methods=['DELETE'])
@Auth.auth_required
def delete_todo(current_user, todo_id):
	"""
	Delete a specific todo item for a user
	:param current_user:
	:param todo_id:
	:return:
	"""
	return Todo.delete_todo(current_user.id, todo_id)
