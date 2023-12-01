import os
from flask import Flask
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

from App.models.admin import Admin

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    jwt_authenticate_admin,
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
         
@admin_views.route('/students', methods=['POST'])
@jwt_required()
def add_students():
  if not jwt_current_user or not isinstance(jwt_current_user, Admin):
      return 'Unauthorized', 401
  
  # Check if the POST request has a file
  if 'file' not in request.files:
      return jsonify({'error': 'No file selected'}), 400
  
  file = request.files['file']

  if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
  
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the content of the file
    with open(file_path, 'r') as fp:
        file_content = fp.read()
  '''
        for row in file:
          id=row['id']
          student=Student.query.get(id) 
          if student:
            flash('error':f"ID already exists {row['id']}"), 400
          elif row['studentType'] != "Full-Time" or row['studentType'] != "Part-Time" or row['studentType'] != "Evening" or or row['studentType'] != "Graduated" or row['studentType'] != "On-Leave"
            flash('error':f"{row['studentType']} was not a valis option"), 400
          else:
          add_student_information(admin=user,id=row['id'],firstname=row['firstname'],lastname=row['lastname'],studentType=row['studentType'],yearofEnrollmentrow=row['yearofEnrollment'])
      flash('database Updated')'''
  
  return jsonify({'message': file_content}), 200

@admin_views.route('/students', methods=['PUT'])
def update_students():
  return jsonify({'message': f"Students updated"})
