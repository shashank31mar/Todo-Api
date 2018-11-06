# Todo-Api
# Requirements:
  Python 3.7
# DB Migration Commands
1) python manage.py db init
2) python manage.py db migrate

After this two table must have been created
1) todo
2) user

Although todo_sqlite file is already added, so no need to run migration commands as of now

# Run Application
Export Following variables in terminal (mentioned in env/environment.env file)
1) FLASK_ENV=development
2) JWT_SECRET_KEY=shashank

Run run.py file to startup the application.
# Api Endpoints
Admin Reponsibilites:
1) /user - get all users
2) /user/register - register a new user
3) /user/<id> - get user with public id
4) /user/<id> - promote user to admin PUT request
5) /user/<id> - delete user, DELTE request
 
Todo Endpoints:
1) /todo - get todo's for logged in user
2) /todo/<id> - get specific todo for logged in user
3) /todo - create new todo 
4) /todo/<id> - complete todo, PUT request
5) /todo/u - update todo, POST request
6) /todo/<id> - dlete request todo, DELTE request
  
1) /login - logins in the user, and return the token for further use
