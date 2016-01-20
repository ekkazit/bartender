from math import ceil
from time import strftime
from datetime import datetime
from flask import Blueprint, jsonify, request, g, json
from sqlalchemy import text
from sqlalchemy.sql import or_, and_
from pospax import db
from app.models import Bill, BillItem, Status, Receipt
from app.schema import BillSchema, ReceiptSchema

bill_api = Blueprint('bill_api', __name__, url_prefix='/api/bill')


def get_num(v):
	if v: return float(v.replace(',', ''))
	return 0


@bill_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1
	g.uid = 1
	g.tax = 7
	g.currency = 'THB'
	g.bigit = 5
	g.discount_rate = 0


@bill_api.route('/new')
def bill_new():
	no = db.session.query(db.func.max(Bill.no)).filter_by(site_id=g.sid, branch_id=g.bid).scalar() or 0
	ref_no = no + 1
	bill_no = strftime('%Y%m') + '-' + str(ref_no).zfill(g.bigit)
	status = Status.query.filter_by(name='new', module='bill').first()

	bill = Bill(site_id=g.sid, branch_id=g.bid)
	bill.no = ref_no
	bill.bill_no = bill_no
	bill.status_id = status.id
	bill.currency = g.currency
	bill.user_id = g.uid
	bill.tax_rate = g.tax
	bill.discount_rate = g.discount_rate

	bill_count = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid, status_id=status.id).count()
	data, error = BillSchema().dump(bill)
	return jsonify({
		'bill': data,
		'hold_bill_count': bill_count
	})


@bill_api.route('/hold')
def bill_hold():
	hold_bills = []
	status = Status.query.filter_by(name='new', module='bill').first()
	if status:
		hold_bills = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid,
			status_id=status.id
		).order_by(text('bill_date desc')).order_by(text('bill_date asc')).all()
	data, error = BillSchema(many=True).dump(hold_bills)
	return jsonify({ 'hold_bills': data })


@bill_api.route('/open/<id>')
def bill_open(id):
	bill = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	data, error = BillSchema().dump(bill)
	return jsonify({ 'bill': data })


@bill_api.route('/get', defaults={'id': ''})
@bill_api.route('/get/<id>')
def bill_get(id):
	receipt = None
	if id:
		bill = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
		receipt = Receipt.query.filter_by(bill_id=bill.id).first()
	else:
		no = db.session.query(db.func.max(Bill.no)).filter_by(site_id=g.sid, branch_id=g.bid).scalar() or 0
		ref_no = no + 1
		bill_no = strftime('%Y%m') + '-' + str(ref_no).zfill(g.bigit)
		bill = Bill(site_id=g.sid, branch_id=g.bid)
		bill.no = ref_no
		bill.bill_no = bill_no
	receipt_data = {}
	if receipt:
		receiptSchema = ReceiptSchema()
		receipt_data = receiptSchema.dump(receipt).data
	schema = BillSchema()
	return jsonify({
		'bill': schema.dump(bill).data,
		'receipt': receipt_data
	})


@bill_api.route('/next', defaults={'id': ''})
@bill_api.route('/next/<id>')
def bill_get_next(id):
	next_id = db.session.query(db.func.min(Bill.id)).filter_by(site_id=g.sid, branch_id=g.bid).filter(Bill.id > id).scalar() or 0
	max_id = db.session.query(db.func.max(Bill.id)).filter_by(site_id=g.sid, branch_id=g.bid).scalar() or 0
	return jsonify({ 'next_id': next_id, 'max_id': max_id })


@bill_api.route('/prev', defaults={'id': ''})
@bill_api.route('/prev/<id>')
def bill_get_prev(id):
	prev_id = db.session.query(db.func.max(Bill.id)).filter_by(site_id=g.sid, branch_id=g.bid).filter(Bill.id < id).scalar() or 0
	min_id = db.session.query(db.func.min(Bill.id)).filter_by(site_id=g.sid, branch_id=g.bid).scalar() or 0
	return jsonify({ 'prev_id': prev_id, 'min_id': min_id })


@bill_api.route('/delete/<id>')
def bill_delete(id):
	result = 0
	bill = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	if bill:
		result = int(id)
		Receipt.query.filter_by(bill_id=id).delete()
		BillItem.query.filter_by(bill_id=id).delete()
		Bill.query.filter_by(id=id).delete()
		db.session.commit()
	return jsonify({ 'result': result })


def bill_prepare_save(frm, frm_items):
	result = 0

	forms = {
		'branch_id': g.bid,
		'site_id': g.sid,
		'user_id': g.uid,
		'bill_no': frm.get('bill_no') or '',
		'currency': frm.get('currency'),
		'cust_id': frm.get('cust_id') or None,
		'no': frm.get('no'),
		'receipt_no': frm.get('receipt_no') or None,
		'remark': frm.get('remark') or '',
		'status_id': frm.get('status_id') or None,
		'table_id': frm.get('table_id') or None,
		'tax_rate': frm.get('tax_rate') or 0,
		'discount_rate': frm.get('discount_rate') or 0,
		'total_amount': frm.get('total_amount') or 0,
		'total_discount': frm.get('total_discount') or 0,
		'total_price': frm.get('total_price') or 0,
		'total_tax': frm.get('total_tax') or 0,
		'total_qty': frm.get('total_qty') or 0,
	}

	id = frm.get('id') or None
	if id:
		bill = Bill.query.get(id)
		for k, v in forms.iteritems():
			setattr(bill, k, v)
		db.session.merge(bill)
	else:
		bill = Bill()
		for k, v in forms.iteritems():
			setattr(bill, k, v)
		db.session.add(bill)
	db.session.commit()

	if bill.id:
		result = bill.id
		BillItem.query.filter_by(bill_id=bill.id).delete()
		for elem in frm_items:
			bill_item = BillItem()
			for k, v in elem.iteritems():
				try:
					if k == 'id': continue
					setattr(bill_item, k, v)
				except: pass
			bill_item.bill_id = bill.id
			db.session.add(bill_item)
		db.session.commit()
	return result


@bill_api.route('/save', methods=['GET', 'POST'])
def bill_save():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	frm = f['bill']
	frm_items = frm['bill_items']
	result = bill_prepare_save(frm, frm_items)
	return jsonify({ 'result': result })


@bill_api.route('/checkout', methods=['GET', 'POST'])
def bill_checkout():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	frm = f['bill']
	frm_items = frm['bill_items']
	result = bill_prepare_save(frm, frm_items)

	checkforms = f['checkout']
	if result and checkforms:
		# delete old receipts
		Receipt.query.filter_by(bill_id=result).delete()
		# create new receipts
		receipt = Receipt(site_id=g.sid, branch_id=g.bid, bill_id=result)
		receipt.line_no = 1
		receipt.receipt_no = 'R' + frm['bill_no']
		receipt.method = 'cash'
		receipt.total_amount = checkforms.get('total_amount') or 0
		receipt.total_charge = checkforms.get('total_charge') or 0
		receipt.total_return = checkforms.get('total_return') or 0
		db.session.add(receipt)
		db.session.commit()
		# update bill status
		status = Status.query.filter_by(name='paid', module='bill').first()
		bill = Bill.query.get(result)
		if bill:
			bill.status_id = status.id
			db.session.merge(bill)
			db.session.commit()
	return jsonify({ 'result': result })


@bill_api.route('/complete/<id>')
def bill_complete(id):
	result = 0
	bill = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	if bill:
		status = Status.query.filter_by(name='complete', module='bill').first()
		bill.status_id = status.id
		result = bill.id
		db.session.merge(bill)
		db.session.commit()
	return jsonify({'result': result})


@bill_api.route('/search', methods=['POST'])
def bill_search():
	f = request.get_json()
	if f is None:
		f = request.form
	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	sort = f.get('sort') or None
	desc = f.get('desc') or False
	from_date = f.get('from_date') or None
	to_date = f.get('to_date') or None
	status = f.get('status') or None
	query = Bill.query.filter_by(site_id=g.sid, branch_id=g.bid)
	# filter by bill no
	if term:
		query = query.filter(or_(Bill.bill_no.ilike('%' + term + '%')))
	# filter by from and to date
	if from_date:
		query = query.filter(Bill.bill_date >= datetime.strptime(from_date, '%d/%m/%Y'))
	if to_date:
		query = query.filter(Bill.bill_date <= datetime.strptime(to_date + ' 23:59:59', '%d/%m/%Y %H:%M:%S'))
	# filter by status id
	if status:
		query = query.filter_by(status_id=int(status))
	# sort and order result items
	if sort:
		query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))
	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total
	bills = query.limit(rp).offset((page - 1) * rp)
	schema = BillSchema(many=True)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'bills': schema.dump(bills).data
	})


@bill_api.route('/formsave', methods=['GET', 'POST'])
def bill_form_save():
	f = request.get_json()
	if f is None:
		f = request.form

	forms = {
		'branch_id': g.bid,
		'site_id': g.sid,
		'user_id': g.uid,
		'bill_no': f.get('bill_no') or '',
		'currency': f.get('currency'),
		'cust_id': f.get('cust_id') or None,
		'no': f.get('no'),
		'receipt_no': f.get('receipt_no') or None,
		'remark': f.get('remark') or '',
		'status_id': f.get('status_id') or None,
		'table_id': f.get('table_id') or None,
		'tax_rate': f.get('tax_rate') or 0,
		'discount_rate': get_num(f.get('discount_rate')),
		'total_amount': get_num(f.get('total_amount')),
		'total_discount': get_num(f.get('total_discount')),
		'total_price': get_num(f.get('total_price')),
		'total_tax': get_num(f.get('total_tax')),
		'total_qty': get_num(f.get('total_qty')),
	}

	# update bill
	bill = None
	id = f.get('id') or None
	if id:
		bill = Bill.query.get(id)
		for k, v in forms.iteritems():
			setattr(bill, k, v)
		db.session.merge(bill)
	else:
		bill = Bill()
		for k, v in forms.iteritems():
			setattr(bill, k, v)
		db.session.add(bill)
	db.session.commit()

	# update bill items
	bill_items = json.loads(f.get('bill_items'))
	if bill.id:
		result = bill.id
		BillItem.query.filter_by(bill_id=bill.id).delete()
		for elem in bill_items:
			bill_item = BillItem()
			for k, v in elem.iteritems():
				try:
					if k == 'id': continue
					setattr(bill_item, k, v)
				except: pass
			bill_item.bill_id = bill.id
			db.session.add(bill_item)
		db.session.commit()

	# update receipt info
	rcv = f.get('receipt_no') or None
	if bill.id and rcv:
		Receipt.query.filter_by(site_id=g.sid, branch_id=g.bid, bill_id=result).delete()
		receipt = Receipt(site_id=g.sid, branch_id=g.bid, bill_id=result)
		receipt.line_no = 1
		receipt.receipt_no = f.get('receipt_no') or ''
		receipt.method = f.get('method') or ''
		receipt.total_amount = get_num(f.get('total_amount'))
		receipt.total_charge = get_num(f.get('total_rcv_charge'))
		receipt.total_return = get_num(f.get('total_rcv_return'))
		db.session.add(receipt)
		db.session.commit()
	return jsonify({'result': bill.id})
