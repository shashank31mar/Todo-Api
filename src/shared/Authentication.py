import jwt
import os
import datetime
from flask import json, Response, request, g, make_response
from src.model.UserModel import User
from functools import wraps
from flask import jsonify


class Auth:
	"""
	Auth Class
	"""

	@staticmethod
	def generate_token(user_id):
		"""
		Generate Token Method
		:param user_id:
		:return:
		"""
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
				'iat': datetime.datetime.utcnow(),
				'public_id': user_id
			}
			print(os.getenv('JWT_SECRET_KEY'))
			token = jwt.encode(
				payload,
				os.getenv('JWT_SECRET_KEY'),
				'HS256'
			).decode("utf-8")

			return jsonify({'token': token})

		except Exception:
			return make_response('Could not generate token', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

	@staticmethod
	def decode_token(token):
		"""
		Decode Token Method
		:param token:
		:return:
		"""
		re = {'data': {}, 'error': {}}
		try:
			payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
			re['data'] = {'public_id': payload['public_id']}
			return re
		except jwt.ExpiredSignatureError as e1:
			re['error'] = {'message': 'token expired, please login again'}
			return re
		except jwt.InvalidTokenError:
			re['error'] = {'message': 'Invalid token, please try again with a new token'}
		return re

	# decorator
	@staticmethod
	def auth_required(func):
		"""
		Auth decorator
		"""

		@wraps(func)
		def decorated_auth(*args, **kwargs):
			if 'api-token' not in request.headers:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'token missing!'}),
					status=400
				)
			token = request.headers.get('api-token')
			data = Auth.decode_token(token)

			if data['error']:
				return Response(
					mimetype="application/json",
					response=json.dumps(data['error']),
					status=400
				)

			public_id = data['data']['public_id']
			check_user = User.get_one_user(public_id)
			if not check_user:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'user does not exist, invalid token'}),
					status=400
				)
			g.user = {'public_id': public_id}
			current_user = User.query.filter_by(public_id=data['data']['public_id']).first()
			return func(current_user, *args, **kwargs)

		return decorated_auth
