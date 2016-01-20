from pospax import db

def execute_table_migrations():
	db.drop_all()
	db.create_all()
	print 'All tables migrated'
