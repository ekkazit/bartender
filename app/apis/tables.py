from math import ceil
from flask import Blueprint, jsonify, request, g
from sqlalchemy import text
from sqlalchemy.sql import or_
from pospax import db
from app.models import Table
from app.schema import TableSchema

table_api = Blueprint('table_api', __name__, url_prefix='/api/table')
tableSchema = TableSchema(many=True)


@table_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@table_api.route('/list')
def table_list():
	tables = Table.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y').all()
	return jsonify({
		'tables': tableSchema.dump(tables).data
	})


@table_api.route('/get', defaults={'id': ''})
@table_api.route('/get/<id>')
def table_get(id):
	table = Table(site_id=g.sid, branch_id=g.bid)
	if id:
		table = Table.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y', id=id).first()
	schema = TableSchema()
	return jsonify({
		'table': schema.dump(table).data
	})


@table_api.route('/delete/<id>')
def table_delete(id):
	result = 0
	table = Table.query.filter_by(site_id=g.sid, branch_id=g.bid, id=id).first()
	if table:
		result = table.id
		if table.is_active == 'N':
			db.session.delete(table)
		else:
			table.is_active = 'N'
			db.session.merge(table)
		db.session.commit()
	return jsonify({ 'result': result })


@table_api.route('/save', methods=['POST'])
def table_save():
	result = 0
	f = request.get_json()
	if f is None:
		f = request.form

	forms = {
		'site_id': g.sid,
		'branch_id': g.bid,
		'name': f.get('name') or '',
		'description': f.get('description') or '',
		'seats': f.get('seats') or 0,
		'floor': f.get('floor') or 0
	}

	id = f.get('id') or None
	if id:
		table = Table.query.get(id)
		for k, v in forms.iteritems():
			setattr(table, k, v)
		db.session.merge(table)
	else:
		table = Table()
		for k, v in forms.iteritems():
			setattr(table, k, v)
		db.session.add(table)
	db.session.commit()

	if table: result = table.id
	return jsonify({ 'result': result })


@table_api.route('/search', methods=['POST'])
def table_search():
	f = request.get_json()
	if f is None:
		f = request.form

	page = f.get('page') or 1
	rp = f.get('rp') or 10
	term = f.get('term') or ''
	sort = f.get('sort') or None
	desc = f.get('desc') or False
	active = f.get('is_active') or 'Y'

	query = Table.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active=active)
	if term:
		query = query.filter(or_(
			Table.name.ilike('%' + term + '%'),
			Table.description.ilike('%' + term + '%'),
		))

	if sort:
		query = query.order_by(text(sort + ' ' + ('desc' if desc else 'asc')))

	total = query.count()
	total_pages = int(ceil(float(total) / rp))
	results = page * rp
	page_count = results if results <= total else total

	tables = query.limit(rp).offset((page - 1) * rp)
	return jsonify({
		'total': total,
		'total_pages': total_pages,
		'page_count': page_count,
		'tables': tableSchema.dump(tables).data
	})


@table_api.route('/term', methods=['POST'])
def table_term():
	f = request.get_json()
	if f is None:
		f = request.form
	term = f.get('q') or None
	query = Table.query.filter_by(site_id=g.sid, branch_id=g.bid, is_active='Y')
	if term:
		query = query.filter(or_(
			Table.name.ilike('%' + term + '%'),
			Table.description.ilike('%' + term + '%'),
		))
	tables = query.all()
	return jsonify({
		'tables': tableSchema.dump(tables).data
	})
