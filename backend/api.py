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
        }),200
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
- Get Skills by Status
""" 

@api.route("/skill/<string:status>")
def getskillbystatus(status):
    skill_list = Skill.query.filter_by(Skill_Status=status).all()
    #skill_list = Skill.query.all()
    if len(skill_list):
        return jsonify({
            "code": 200,
            "data":{
                "Skill_List": [skill.json() for skill in skill_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no available skill."
    }),404
    

########################################################

"""
Job Role
- Create
"""

#Create A Job Role
@api.route("/jobrole", methods=['POST'])
def createjobrole():    
    data = request.get_json()
    name = data["Job_Role_Name"]
    desc = data["Job_Role_Desc"]
    ## job status default active
   
    jobrole = JobRole.query.filter_by(Job_Role_Name=name).first()
    
    if (jobrole):  ##frontend - access by error.response.data.code == 400
        return jsonify({
            "code": 400,
            "data": jobrole.json(),            
            "message": "Job Role already existed"
        }), 400
    
    jobrole = JobRole(name,desc)
    
    try: 
        db.session.add(jobrole)
        db.session.commit()
        
        skill_list = data["Job_Role_Skills"]
        for sid in skill_list:
            item = JobRoleSkill(jobrole.Job_Role_ID, sid)
            db.session.add(item)
            db.session.commit()          

    except:
        return jsonify({
            "code": 500,
            "message": "An error occurred creating the Job Role."

        }), 500

    return jsonify(
        {
            "code": 201,
            "data": jobrole.json(),
            "message": f'Job Role has been successfully created!'
        }
    ), 201

#Get Job Role by Status
@api.route("/jobrole/<string:status>")
def getjobrolebystatus(status):
    job_role_list = JobRole.query.filter_by(Job_Role_Status=status).all()
    if len(job_role_list):
        return jsonify({
            "code": 200,
            "data":{
                "Job_Role_List": [jon_role.json() for jon_role in job_role_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no available Job Role."
    }),404


