from flask import Blueprint, render_template, request, g
from app.models import Status
from pospax import app

admin_app = Blueprint('admin_app', __name__, url_prefix='/admin')


@admin_app.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@admin_app.route('/product')
def product():
	return render_template('admin/product/index.html')


@admin_app.route('/product/form', defaults={'id': ''})
@admin_app.route('/product/form/<id>')
def admin_product_form(id):
	return render_template('admin/product/form.html', id=id)


@admin_app.route('/category')
def admin_category():
	return render_template('admin/category/index.html')


@admin_app.route('/category/form', defaults={'id': ''})
@admin_app.route('/category/form/<id>')
def admin_category_form(id):
	return render_template('admin/category/form.html', id=id)


@admin_app.route('/table')
def admin_table():
	return render_template('admin/table/index.html')


@admin_app.route('/table/form', defaults={'id': ''})
@admin_app.route('/table/form/<id>')
def admin_table_form(id):
	return render_template('admin/table/form.html', id=id)


@admin_app.route('/customer')
def admin_customer():
	return render_template('admin/customer/index.html')


@admin_app.route('/customer/form', defaults={'id': ''})
@admin_app.route('/customer/form/<id>')
def admin_customer_form(id):
	return render_template('admin/customer/form.html', id=id)


@admin_app.route('/user')
def admin_user():
	return render_template('admin/user/index.html')


@admin_app.route('/user/form', defaults={'id': ''})
@admin_app.route('/user/form/<id>')
def admin_user_form(id):
	return render_template('admin/user/form.html', id=id)


@admin_app.route('/branch')
def admin_branch():
	return render_template('admin/branch/index.html')


@admin_app.route('/branch/form', defaults={'id': ''})
@admin_app.route('/branch/form/<id>')
def admin_branch_form(id):
	return render_template('admin/branch/form.html', id=id)


@admin_app.route('/orders')
def admin_orders():
	status = Status.query.filter_by(is_active='Y')
	return render_template('admin/orders/index.html', status=status)


@admin_app.route('/orders/form', defaults={'id': ''})
@admin_app.route('/orders/form/<id>')
def admin_orders_form(id):
	report_server = app.config['REPORT_SERVER_URL']
	return render_template('admin/orders/form.html', id=id, rpt_server=report_server, site_id=g.sid)
