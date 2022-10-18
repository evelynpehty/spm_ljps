"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, request, jsonify
from models import db, Role, Staff, JobRole, Skill, JobRoleSkill, Course, CourseSkill, LearningJourney, LearningJourneyItem, Registration

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
- Create Skill 
- Get Skills by ID
- Get Skills by Status
- Get All Skills (SPM8 - View Job Role Details, need to get all skills information)
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
            "message": "Skill has been successfully created!"

        }
    ), 201  

#Get Skill by ID
@api.route("/skill/<int:id>")
def getskillbyid(id):
    skill = Skill.query.filter_by(Skill_ID=id).first()
    if skill:
        return jsonify({
            "code": 200,
            "data": skill.json()
            
        }), 200
    return jsonify({
        "code": 404,
        "message": "No such skill record found"
    }),404

#Get all Skills by status
@api.route("/skill/<string:status>")
def getskillbystatus(status):
    skill_list = Skill.query.filter_by(Skill_Status=status).all()
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
    
# Get All Skills (SPM8 - View Job Role Details, need to get all skills information)
@api.route("/skill")
def getallskills():
    skill_list = Skill.query.all()
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
- Create Job Role
- Get Job Role by ID
- Get Job Role by Status
- SPM-47: View All Job Roles
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
    
@api.route("/jobrole/<int:id>")
def getjobrolebyid(id):
    jobrole = JobRole.query.filter_by(Job_Role_ID=id).first()
    if jobrole:
        return jsonify({
            "code": 200,
            "data": jobrole.json()
            
        }), 200
    return jsonify({
        "code": 404,
        "message": "No such jobrole record found"
    }),404

#Get Job Role by Status
@api.route("/jobrole/<string:status>")
def getjobrolebystatus(status):
    job_role_list = JobRole.query.filter_by(Job_Role_Status=status).all()
    if len(job_role_list):
        return jsonify({
            "code": 200,
            "data":{
                "Job_Role_List": [job_role.json() for job_role in job_role_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no available Job Role."
    }),404

#Get Job Role Details (SPM-47: View All Job Roles)
@api.route("/jobrole")
def getalljobrole():
    job_role_list = JobRole.query.all()
    if len(job_role_list):
        return jsonify({
            "code": 200,
            "data":{
                "Job_Role_List": [job_role.json() for job_role in job_role_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no available Job Role."
    }),404

########################################################
"""
Course 
- Get All Active Course
"""
#Get Course by ID - needed for View Skill Details
#need to do route course/id as courseid is string eg. COR001, conflicts with /course/<string:status>
@api.route("/course/id/<string:id>")
def getjobcoursebyid(id):
    course = Course.query.filter_by(Course_ID=id).first()

    if course:
        return jsonify({
            "code": 200,
            "data": course.json()  
        }), 200

    return jsonify({
        "code": 404,
        "message": "No such course record found"
    }), 404

#Get course by status
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

########################################################
"""
Learning Journey 
- Create Learning Journey
- Get Learning Journey by Staff
"""

@api.route("/learningjourney", methods=['POST'])
def createlearningjourney():    
    data = request.get_json()
    staffid = data["Staff_ID"]
    jobroleid = data["Job_Role_ID"]

    lj = LearningJourney(staffid,jobroleid)
    
    try: 
        db.session.add(lj)
        db.session.commit()
        
        course_list = data["Course_List"]
        for cid in course_list:
            item = LearningJourneyItem(lj.Learning_Journey_ID, cid)
            db.session.add(item)
            db.session.commit()          

    except:
        return jsonify({
            "code": 500,
            "message": "An error occurred creating the learning journey"

        }), 500

    return jsonify(
        {
            "code": 201,
            "data": lj.json(),
            "message": f'Learning Journey has been successfully created!'
        }
    ), 201
    
@api.route("/learningjourney/<int:staffid>")
def getlearningjourneybystaff(staffid):
    learningjourney_list = LearningJourney.query.filter_by(Staff_ID=staffid).all()
    if len(learningjourney_list):
        return jsonify({
            "code": 200,
            "data":{
                "LearningJourney_List": [lj.json() for lj in learningjourney_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "No Available Learning Journey"
    }),404  
    
########################################################
"""
Registration 
- Get Course Registration by staffid
"""

@api.route("/registration/<int:staffid>")
def getregistrationbystaff(staffid):
    registration_list = Registration.query.filter_by(Staff_ID=staffid).all()
    if len(registration_list):
        return jsonify({
            "code": 200,
            "data":{
                "Registration_List": [r.json() for r in registration_list]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no registration"
    }),404

########################################################