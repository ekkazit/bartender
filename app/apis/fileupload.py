import os
import uuid
from flask import Blueprint, jsonify, request
from PIL import Image
from pospax import app

fileupload_api = Blueprint('fileupload_api', __name__, url_prefix='/api/fileupload')
allow_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in allow_extensions


@fileupload_api.route('/save', methods=['POST'])
def upload():
	if request.files:
		file = request.files['file']

	if file and allowed_file(file.filename):
		file_name, extension = os.path.splitext(file.filename)
		file_name = str(uuid.uuid4()) + '' + extension
		file_path = os.path.join(app.config['UPLOAD_PATH'], file_name)
		file.save(file_path)
		if os.path.isfile(file_path):
			im = Image.open(file_path)
			imaged = im.resize((400, 400), Image.ANTIALIAS)
			imaged.save(file_path, quality=100)
		path = file_path
		path = '/' + path[path.find('pospax') + 7:]
	return jsonify({'img': file_name or '', 'img_path': path or ''})
