"""
models.py
- Data classes for the application
"""

from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## ROLE ##
class Role(db.Model):
    __tablename__ = 'role'

    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)
    
    #staff = db.relationship('Staff', backref='staff', cascade='all,delete-orphan')

    def __init__(self, Role_Name):
        self.Role_Name = Role_Name

    def json(self):
        return {"Role_ID": self.Role_ID, "Role_Name": self.Role_Name}
        

## STAFF ##
class Staff(db.Model):
    __tablename__ = 'staff'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.ForeignKey('role.Role_ID', ondelete='CASCADE'), nullable=False)
    
    #regi = db.relationship('Registration', backref='regi', cascade='all,delete-orphan')
    
    def __init__(self, Staff_FName, Staff_LName, Dept, Email, Role):
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Email = Email
        self.Role = Role

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                "Staff_ID": self.Staff_ID, 
                "Staff_FName": self.Staff_FName,
                "Staff_LName": self.Staff_LName,
                "Email": self.Email,
                "Dept": self.Dept,
                "Role": self.Role,
            }
    
    
## COURSE ##
class Course(db.Model):
    __tablename__ = 'course'

    Course_ID = db.Column(db.String(20), primary_key=True)
    Course_Name = db.Column(db.String(50), nullable=False)
    Course_Desc = db.Column(db.String(255), nullable=False)
    Course_Status = db.Column(db.String(15), nullable=False)
    Course_Type = db.Column(db.String(10), nullable=False)
    Course_Category = db.Column(db.String(50), nullable=True)
    
    def __init__(self, Course_Name, Course_Desc, Course_Status, Course_Type, Course_Category):
        self.Course_Name = Course_Name
        self.Course_Desc = Course_Desc
        self.Course_Status = Course_Status
        self.Course_Type = Course_Type
        self.Course_Category = Course_Category

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                    "Course_ID": self.Course_ID, 
                    "Course_Name": self.Course_Name,
                    "Course_Desc": self.Course_Desc,
                    "Course_Status": self.Course_Status,
                    "Course_Type": self.Course_Type,
                    "Course_Category": self.Course_Category
                }


## Registration ##
class Registration(db.Model):
    __tablename__ = 'registration'

    Reg_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.String(20), db.ForeignKey('course.Course_ID'))
    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID'))
    Reg_Status = db.Column(db.String(20), nullable=False)
    Completion_Status = db.Column(db.String(20), nullable=False)

    def __init__(self, Course_ID, Staff_ID, Reg_Status, Completion_Status):
        self.Course_ID = Course_ID
        self.Staff_ID = Staff_ID
        self.Reg_Status = Reg_Status
        self.Completion_Status = Completion_Status

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                    "Reg_ID": self.Reg_ID, 
                    "Course_ID": self.Course_ID,
                    "Staff_ID": self.Staff_ID,
                    "Reg_Status": self.Reg_Status,
                    "Completion_Status": self.Completion_Status
                }
        
## Job Role ##
class JobRole(db.Model):
    __tablename__ = 'job_role'

    Job_Role_ID = db.Column(db.Integer, primary_key=True)
    Job_Role_Name = db.Column(db.String(50), nullable=False)
    Job_Role_Desc = db.Column(db.String(255), nullable=False)
    Job_Role_Status = db.Column(db.String(15), nullable=False, default = 'Active')
    
    skill_list = db.relationship('JobRoleSkill', backref='skill_list', cascade='all,delete-orphan')

    def __init__(self, Job_Role_Name, Job_Role_Desc):
        self.Job_Role_Name = Job_Role_Name
        self.Job_Role_Desc = Job_Role_Desc
        #self.Job_Role_Status = Job_Role_Status

    # specify how to represent our book object as a JSON string
    def json(self):
        dto = {
                "Job_Role_ID": self.Job_Role_ID,
                "Job_Role_Name": self.Job_Role_Name,
                "Job_Role_Desc": self.Job_Role_Desc,
                "Job_Role_Status": self.Job_Role_Status
            }
        
        dto["SkillList"] = []
        for item in self.skill_list:
            dto['SkillList'].append(item.json())
            
        return dto
        
## SKILL ##
class Skill(db.Model):
    __tablename__ = 'skill'

    Skill_ID = db.Column(db.Integer, primary_key=True)
    Skill_Name = db.Column(db.String(20), nullable=False)
    Skill_Status = db.Column(db.String(15), nullable=False, default = 'Active')
    
    jobrolelist = db.relationship('JobRoleSkill', backref='jobrolelist', cascade='all,delete-orphan')
    courselist = db.relationship('CourseSkill', backref='courselist', cascade='all,delete-orphan')

    def __init__(self, Skill_Name):
        self.Skill_Name = Skill_Name
        #self.Skill_Status = Skill_Status

    # specify how to represent our book object as a JSON string
    def json(self):
        dto = {
                "Skill_ID": self.Skill_ID,
                "Skill_Name": self.Skill_Name,
                "Skill_Status": self.Skill_Status
            }
        
        dto["Job_List"] = []
        for item in self.jobrolelist:
            dto['Job_List'].append(item.json())
            
        dto["Course_List"] = []
        for c in self.courselist:
            dto['Course_List'].append(c.json())
            
        return dto
               
class JobRoleSkill(db.Model):
    __tablename__ = 'job_role_skill'

    Job_Role_ID = db.Column(db.Integer, db.ForeignKey('job_role.Job_Role_ID'), primary_key=True)
    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID'), primary_key=True)

    def __init__(self, Job_Role_ID, Skill_ID):
        self.Job_Role_ID = Job_Role_ID
        self.Skill_ID = Skill_ID

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                "Job_Role_ID": self.Job_Role_ID,
                "Skill_ID": self.Skill_ID
            }
        
class CourseSkill(db.Model):
    __tablename__ = 'course_skill'

    Course_ID = db.Column(db.String(20), db.ForeignKey('course.Course_ID'), primary_key=True)
    Skill_ID = db.Column(db.Integer, db.ForeignKey('skill.Skill_ID'), primary_key=True)
    

    def __init__(self, Course_ID, Skill_ID):
        self.Course_ID = Course_ID
        self.Skill_ID = Skill_ID

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                "Course_ID": self.Course_ID,
                "Skill_ID": self.Skill_ID
            }

class LearningJourney(db.Model):
    __tablename__ = 'learning_journey'
    Learning_Journey_ID = db.Column(db.Integer, primary_key=True)
    Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID'))
    Job_Role_ID = db.Column(db.Integer, db.ForeignKey('job_role.Job_Role_ID'))
    
    lji = db.relationship('LearningJourneyItem', backref='lji', cascade='all,delete-orphan')

    def __init__(self, Staff_ID, Job_Role_ID):
        self.Staff_ID = Staff_ID
        self.Job_Role_ID = Job_Role_ID
    
    # specify how to represent our book object as a JSON string
    def json(self):
        dto = {
                "Learning_Journey_ID": self.Learning_Journey_ID,
                "Staff_ID": self.Staff_ID,
                "Job_Role_ID": self.Job_Role_ID
            }
        
        dto['CourseList'] = []
        for item in self.lji:
            dto['CourseList'].append(item.json())
            
        return dto
        
class LearningJourneyItem(db.Model):
    __tablename__ = 'learning_journey_item'
    Learning_Journey_ID = db.Column(db.Integer, db.ForeignKey('learning_journey.Learning_Journey_ID'), primary_key=True)
    #Staff_ID = db.Column(db.Integer, db.ForeignKey('staff.Staff_ID'), primary_key=True)
    #Job_Role_ID = db.Column(db.Integer, db.ForeignKey('job_role.Job_Role_ID'), primary_key=True)
    Course_ID = db.Column(db.String(20), db.ForeignKey('course.Course_ID'), Primary_key=True)

    def __init__(self, Learning_Journey_ID, Course_ID):
        self.Learning_Journey_ID = Learning_Journey_ID
        self.Course_ID = Course_ID

    # specify how to represent our book object as a JSON string
    def json(self):
        return {
                "Course_ID": self.Course_ID
            }