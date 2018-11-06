from base64 import b64encode
import json

def test_login(client):
	headers = {
		'Authorization': 'Basic Auth %s' % b64encode("{0}:{1}".format('admin', 'admin').encode('utf-8'))
	}
	data = {
		'username': 'admin',
		'password': 'admin'
	}
	response = client.post('/login', data=json.dumps(data), content_type='application/json')
	print(response.data)
	assert response.status_code == 200


'''
@pytest.fixture
def test_login(self):
	env_name = os.getenv('FLASK_ENV')
	print(env_name)
	app = create_app(env_name)
	tester = app.test_client(self)
	tester.testing = True
	headers = {
		'Authorization': 'Basic %s' % b64encode("{0}:{1}".format('admin', 'admin').encode('utf-8'))
	}
	response = tester.get('/login', headers=headers)
	print(response)
	self.assertEqual(200, response.status_code)
'''