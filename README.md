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
