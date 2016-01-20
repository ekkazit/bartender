import server
from pospax import app
from app.migrations import dbmigrate, seeders
from flask_script import Manager

manager = Manager(app)


@manager.command
def seed():
	seeders.generate_sample_data()


@manager.command
def migrate():
	dbmigrate.execute_table_migrations()


@manager.command
def runserver():
	server.runserver()


if __name__ == '__main__':
	manager.run()
