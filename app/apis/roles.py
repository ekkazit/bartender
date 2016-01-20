from flask import Blueprint, jsonify, request, g
from app.models import Role
from app.schema import RoleSchema

role_api = Blueprint('role_api', __name__, url_prefix='/api/role')
roleSchema = RoleSchema(many=True)


@role_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@role_api.route('/list')
def role_list():
	roles = Role.query.filter_by(is_active='Y').all()
	return jsonify({
		'roles': roleSchema.dump(roles).data
	})
