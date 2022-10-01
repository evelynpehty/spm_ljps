"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, request, jsonify
from models import db, Role, Staff, JobRole, Skill, JobRoleSkill, Course, CourseSkill

api = Blueprint('api', __name__)

########################################################

"""
ROLE
- Get Role by Role_ID
"""
    
#Get Role by Role_ID
@api.route("/role/<int:roleid>")
def getrolebyid(roleid):
    role = Role.query.filter_by(Role_ID = roleid).first()
    if role:
        return jsonify({
            "code": 200,
            "data":role.json()
        })
    return jsonify({
        "code": 404,
        "message": "Role does not exist"
    }),404
    
########################################################

"""
Staff
- Get Staff by Email
"""
#Get Staff by Email
@api.route("/staff/<string:email>")
def getstaffbyemail(email):
    staff = Staff.query.filter_by(Email=email).first()
    if staff:
        return jsonify({
            "code": 200,
            "data": staff.json()
        }),200
    return jsonify({
        "code": 404,
        "message": "No record found"
    }),404
    
