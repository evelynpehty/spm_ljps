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

@api.route("/skill", methods=['POST'])
def create_skill():
    data = request.get_json()

    if (Skill.query.filter_by(Skill_Name=data['Skill_Name']).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Skill_Name": data['Skill_Name']
                },
                "message": "Skill already exists."
            }
        ), 400

    skill = Skill(data['Skill_Name'])

    try:
        db.session.add(skill)
        db.session.flush()

        course_list = data['Course_Skills']
        
        for Course_ID in course_list:
            course_skill = CourseSkill(Course_ID, skill.Skill_ID)
            db.session.add(course_skill)
            db.session.flush()
            
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
            "data": skill.json(),
            "message": "Skill has been successfully created!'

        }
    ), 201  

"""
Course 
- Get All Active Course
"""

@api.route("/course/<string:status>")
def getcoursebystatus(status):
    course_list = Course.query.filter_by(Course_Status=status).all()
    if len(course_list):
        return jsonify({
            "code": 200,
            "data":{
                "Course_List": [course.json() for course in course_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no available course."
    }),404
