from time import strftime
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, g
from pospax import db

dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')

@dashboard_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@dashboard_api.route('/summary')
def dashboard_summary():
	current_date = strftime('%d/%m/%Y')
	sql = """
		select
			sum(total_amount) as total_amount
		from bill
		where site_id=:site_id and to_char(bill_date, 'dd/MM/yyyy')=:bill_date and status_id in (
			select id from status where name='complete' and module='bill'
		)
	"""
	result1 = db.session.execute(sql, {'site_id': g.sid, 'bill_date': current_date}).first()

	sql = """

		select count(*) as total_orders
		from bill
		where site_id=:site_id and to_char(bill_date, 'dd/MM/yyyy')=:bill_date and status_id not in (
			select id from status where name='complete' and module='bill'
		)
	"""
	result2 = db.session.execute(sql, {'site_id': g.sid, 'bill_date': current_date}).first()


	sql = """
		select count(*) as total_customer
		from (
			select distinct cust_id
			from bill
			where site_id=:site_id and to_char(bill_date, 'dd/MM/yyyy')=:bill_date and cust_id is not null
		) as z
	"""
	result3 = db.session.execute(sql, {'site_id': g.sid, 'bill_date': current_date}).first()

	sql = """
		select sum(prd.cost_price) as total_cost
		from bill bil inner join bill_items itm on bil.id=itm.bill_id inner join product prd on itm.product_id=prd.id
		where bil.site_id=:site_id and to_char(bil.bill_date, 'dd/MM/yyyy')=:bill_date and bil.status_id in (
			select id from status where name='complete' and module='bill'
		)
	"""
	result4 = db.session.execute(sql, {'site_id': g.sid, 'bill_date': current_date}).first()

	return jsonify({
		'total_amount': result1[0] or 0,
		'total_orders': result2[0] or 0,
		'total_customer': result3[0] or 0,
		'total_cost': result4[0] or 0,
	})


@dashboard_api.route('/topbranch')
def dashboard_topbranch():
	current_date = strftime('%d/%m/%Y')
	sql = """
		select brh.id, brh.code, brh.name, sum(bil.total_qty) as total_qty, sum(bil.total_amount) as total_amount
		from bill bil
		left join branch brh on bil.branch_id=brh.id
		where bil.site_id=:site_id and to_char(bil.bill_date, 'dd/MM/yyyy')=:bill_date and bil.status_id in (
			select id from status where name='complete' and module='bill'
		) group by brh.id, brh.code, brh.name
		order by total_amount desc
	"""
	results = db.session.execute(sql, {'site_id': g.sid, 'bill_date': current_date}).fetchall()
	rows = []
	for r in results:
		cols = {
			'branch_id': r[0],
			'code': r[1],
			'name': r[2],
			'total_qty': r[3],
			'total_amount': r[4]
		}
		rows.append(cols)
	return jsonify({'branches': rows})


@dashboard_api.route('/topproduct')
def dashboard_topproduct():
	current_date = strftime('%d/%m/%Y')
	sql = """
		select prd.id, prd.code, prd.name, sum(itm.qty) as total_qty, sum(itm.amount) as total_amount
		from bill bil
			inner join bill_items itm on bil.id=itm.bill_id
			inner join product prd on itm.product_id=prd.id
		where bil.site_id=:site_id and to_char(bil.bill_date, 'dd/MM/yyyy')=:bill_date and bil.status_id in (
			select id from status where name='complete' and module='bill'
		)
		group by prd.id, prd.code, prd.name
		order by total_amount desc
		limit 5
	"""
	results = db.session.execute(sql, {'site_id': g.sid, 'bill_date': current_date}).fetchall()
	rows = []
	for r in results:
		cols = {
			'product_id': r[0],
			'code': r[1],
			'name': r[2],
			'total_qty': r[3],
			'total_amount': r[4]
		}
		rows.append(cols)
	return jsonify({'products': rows})


@dashboard_api.route('/weeklychart', methods=['GET', 'POST'])
def dashboard_weeklychart():
	dt = datetime.now()
	start = dt - timedelta(days=dt.weekday())
	end = start + timedelta(days=6)
	sql = """
		select bil.branch_id, brh.code, brh.name,
			sum(case when to_char(bil.bill_date, 'Dy')='Mon' then bil.total_amount else 0 end) as Mon,
			sum(case when to_char(bil.bill_date, 'Dy')='Tue' then bil.total_amount else 0 end) as Tue,
			sum(case when to_char(bil.bill_date, 'Dy')='Wed' then bil.total_amount else 0 end) as Wed,
			sum(case when to_char(bil.bill_date, 'Dy')='Thu' then bil.total_amount else 0 end) as Thu,
			sum(case when to_char(bil.bill_date, 'Dy')='Fri' then bil.total_amount else 0 end) as Fri,
			sum(case when to_char(bil.bill_date, 'Dy')='Sat' then bil.total_amount else 0 end) as Sat,
			sum(case when to_char(bil.bill_date, 'Dy')='Sun' then bil.total_amount else 0 end) as Sun
		from bill bil left join branch brh on bil.branch_id=brh.id
		where
			bil.site_id=:site_id
			and to_char(bil.bill_date, 'dd/MM/yyyy') between :from_date and :to_date
		group by bil.branch_id, brh.code, brh.name
		order by brh.code asc
	"""

	start = start.strftime('%d/%m/%Y')
	end = end.strftime('%d/%m/%Y')
	results = db.session.execute(sql, {
		'site_id': g.sid, 'from_date': start, 'to_date': end}).fetchall()

	categories = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	rows = []
	for r in results:
		cols = {
			'name': r[2],
			'data': [r[3], r[4], r[5], r[6], r[7], r[8], r[9]]
		}
		rows.append(cols)
	return jsonify({
		'series': rows,
		'categories': categories,
		'title': 'Weekly Sale Amount',
		'subtitle': 'From %s To %s' % (start, end)
	})


@dashboard_api.route('/monthlychart', methods=['GET', 'POST'])
def dashboard_monthlychart():
	current_date = strftime('%m/%Y')
	sql = """
		select bil.branch_id, brh.code, brh.name,
			sum(case when to_char(bil.bill_date, 'W')='1' then bil.total_amount else 0 end) as W1,
			sum(case when to_char(bil.bill_date, 'W')='2' then bil.total_amount else 0 end) as W2,
			sum(case when to_char(bil.bill_date, 'W')='3' then bil.total_amount else 0 end) as W3,
			sum(case when to_char(bil.bill_date, 'W')='4' then bil.total_amount else 0 end) as W4,
			sum(case when to_char(bil.bill_date, 'W')='5' then bil.total_amount else 0 end) as W5
		from bill bil left join branch brh on bil.branch_id=brh.id
		where
			bil.site_id=:site_id and to_char(bil.bill_date, 'MM/yyyy')=:bill_date
		group by bil.branch_id, brh.code, brh.name
		order by brh.code asc
	"""
	results = db.session.execute(sql, { 'site_id': g.sid, 'bill_date': current_date}).fetchall()
	categories = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
	rows = []
	for r in results:
		cols = {
			'name': r[2],
			'data': [r[3], r[4], r[5], r[6], r[7]]
		}
		rows.append(cols)
	return jsonify({
		'series': rows,
		'categories': categories,
		'title': 'Monthly Sale Amount',
		'subtitle': 'As of %s' % current_date
	})


@dashboard_api.route('/yearlychart', methods=['GET', 'POST'])
def dashboard_yearlychart():
	current_date = strftime('%Y')
	sql = """
		select bil.branch_id, brh.code, brh.name,
			sum(case when to_char(bil.bill_date, 'MM')='1' then bil.total_amount else 0 end) as M1,
			sum(case when to_char(bil.bill_date, 'MM')='2' then bil.total_amount else 0 end) as M2,
			sum(case when to_char(bil.bill_date, 'MM')='3' then bil.total_amount else 0 end) as M3,
			sum(case when to_char(bil.bill_date, 'MM')='4' then bil.total_amount else 0 end) as M4,
			sum(case when to_char(bil.bill_date, 'MM')='5' then bil.total_amount else 0 end) as M5,
			sum(case when to_char(bil.bill_date, 'MM')='6' then bil.total_amount else 0 end) as M6,
			sum(case when to_char(bil.bill_date, 'MM')='7' then bil.total_amount else 0 end) as M7,
			sum(case when to_char(bil.bill_date, 'MM')='8' then bil.total_amount else 0 end) as M8,
			sum(case when to_char(bil.bill_date, 'MM')='9' then bil.total_amount else 0 end) as M9,
			sum(case when to_char(bil.bill_date, 'MM')='10' then bil.total_amount else 0 end) as M10,
			sum(case when to_char(bil.bill_date, 'MM')='11' then bil.total_amount else 0 end) as M11,
			sum(case when to_char(bil.bill_date, 'MM')='12' then bil.total_amount else 0 end) as M12
		from bill bil left join branch brh on bil.branch_id=brh.id
		where
			bil.site_id=:site_id and to_char(bil.bill_date, 'yyyy')=:bill_date
		group by bil.branch_id, brh.code, brh.name
		order by brh.code asc
	"""
	results = db.session.execute(sql, { 'site_id': g.sid, 'bill_date': current_date}).fetchall()
	categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	rows = []
	for r in results:
		cols = {
			'name': r[2],
			'data': [r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14]]
		}
		rows.append(cols)
	return jsonify({
		'series': rows,
		'categories': categories,
		'title': 'Yearly Sale Amount',
		'subtitle': 'As of Jan-Dec %s' % current_date
	})
