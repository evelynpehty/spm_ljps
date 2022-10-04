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

########################################################

"""
Skills
- Create Skill 
""" 
#Create Skills
@api.route("/skill/create", methods=['POST'])
def create_skill():
    data = request.get_json()

    if (Skill.query.filter_by(Skill.Skill_Name == data['Skill_Name'].first())):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Skill_Name": Skill.Skill_Name
                },
                "message": "Skill already exists."
            }
        ), 400

    skill = Skill(data['Skill_Name'])

    try:
        db.session.add(skill)
        db.session.commit()

        course_list = data['Course_Skills']
        for Course_ID in course_list:
            course_skill = CourseSkill(Skill.Skill_ID, Course_ID)
            db.session.add(course_skill)
        
        db.session.commit()

    except: 
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the skill."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": skill.json()
        }
    ), 201  