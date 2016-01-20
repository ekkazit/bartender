from flask import Blueprint, jsonify, request, g
from app.models import Status
from app.schema import StatusSchema

status_api = Blueprint('status_api', __name__, url_prefix='/api/status')
statusSchema = StatusSchema(many=True)


@status_api.before_request
def before_request():
	g.sid = 1
	g.bid = 1


@status_api.route('/list')
def status_list():
	status = Status.query.filter_by(is_active='Y').all()
	return jsonify({
		'status': statusSchema.dump(status).data
	})
