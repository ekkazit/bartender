import os
BASEDIR = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(BASEDIR, 'public/temp/')
UPLOAD_PATH = os.path.join(BASEDIR, 'public/upload/')

REPORT_SERVER_URL = 'http://localhost:8080/birt/'

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost/pospax'
SQLALCHEMY_POOL_SIZE = 20

MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'ekkazit@gmail.com'
MAIL_PASSWORD = ''

BLUEPRINTS = [
	'app.apis.product.product_api',
	'app.apis.category.category_api',
	'app.apis.customer.customer_api',
	'app.apis.tables.table_api',
	'app.apis.users.user_api',
	'app.apis.branch.branch_api',
	'app.apis.roles.role_api',
	'app.apis.fileupload.fileupload_api',
	'app.apis.bills.bill_api',
	'app.apis.status.status_api',
	'app.apis.dashboard.dashboard_api',
	'app.modules.pos.pos_app',
	'app.modules.admin.admin_app',
	'app.modules.menus.menu_app',
	'app.modules.home.home_app',
	'app.modules.reports.report_app',
]
