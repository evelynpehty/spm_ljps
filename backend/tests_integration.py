import unittest
import json
from flask_testing import TestCase
from models import db, Role, CourseSkill, JobRoleSkill, JobRole, Skill, Course, Registration, LearningJourney, LearningJourneyItem, Staff
from application import create_app

app = create_app()
class TestApp(TestCase):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        # pass in test configuration
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


"""
Staff
- Get Staff by Email
"""

class TestGetStaffbyEmail(TestApp):
    def test_get_staff_by_email(self):
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="pehtingyu@gmail.com", Role=1)
        st2 = Staff(Staff_FName='Evelyn', Staff_LName='Peh Ting Yu', Dept="Sales", Email="pehtingyu@gmail.com", Role=2)

        db.session.add(st1)
        db.session.add(st2)
        db.session.commit()
        
        response = self.client.get("/api/staff/"+ st1.Email)
        
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Dept": st1.Dept,
                "Email": st1.Email,
                "Role": st1.Role,
                "Staff_FName": st1.Staff_FName,
                "Staff_ID": st1.Staff_ID,
                "Staff_LName": st1.Staff_LName
            }
        })
        
    def test_get_staff_by_nonexistingemail(self):
        response = self.client.get("/api/staff/evelyn@gmail.com")
        
        self.assertEqual(response.json, {
            "code": 404,
            "message": "No record found"
        })

"""
Course 
- Get All Course
- Get Course by ID
- Get Course by Status
"""
class TestGetAllCourses(TestApp):
    def test_get_all_courses(self):
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="Effective Communication", Course_Name="Effective Communication", Course_Desc="Effective Communication", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        response = self.client.get("/api/course")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Course_List": [
                        {
                            "Course_ID": c1.Course_ID, 
                            "Course_Name": c1.Course_Name,
                            "Course_Desc": c1.Course_Desc,
                            "Course_Status": c1.Course_Status,
                            "Course_Type": c1.Course_Type,
                            "Course_Category": c1.Course_Category
                        },
                        {
                            "Course_ID": c2.Course_ID, 
                            "Course_Name": c2.Course_Name,
                            "Course_Desc": c2.Course_Desc,
                            "Course_Status": c2.Course_Status,
                            "Course_Type": c2.Course_Type,
                            "Course_Category": c2.Course_Category
                        }
                    ]
            }
        })
        
    def test_nocourse(self):
        response = self.client.get("/api/course")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no course."
        }) 
        
class TestGetCourseById(TestApp):
    def test_get_course_by_id(self):
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/api/course/id/"+str(c1.Course_ID))

        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                    "Course_ID": c1.Course_ID, 
                    "Course_Name": c1.Course_Name,
                    "Course_Desc": c1.Course_Desc,
                    "Course_Status": c1.Course_Status,
                    "Course_Type": c1.Course_Type,
                    "Course_Category": c1.Course_Category
                }
        })
    
    def test_get_course_by_nonexistingid(self):
        response = self.client.get("/api/course/id/100")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "No such course record found"
        })    


class TestGetCourseByStatus(TestApp):
    def test_get_course_by_ActiveStatus(self):
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR002", Course_Name="Effective Communication", Course_Desc="Effective Communication", Course_Status="Retired", Course_Type="Internal", Course_Category="Core")
        c3 = Course(Course_ID="COR003", Course_Name="Team Building", Course_Desc="Team Building", Course_Status="Pending", Course_Type="Internal", Course_Category="Core")
        
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()

        response = self.client.get("/api/course/Active")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Course_List": [
                        {
                            "Course_ID": c1.Course_ID, 
                            "Course_Name": c1.Course_Name,
                            "Course_Desc": c1.Course_Desc,
                            "Course_Status": c1.Course_Status,
                            "Course_Type": c1.Course_Type,
                            "Course_Category": c1.Course_Category
                        }
                    ]
            }
        })
        
    def test_get_course_by_RetiredStatus(self):
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR002", Course_Name="Effective Communication", Course_Desc="Effective Communication", Course_Status="Retired", Course_Type="Internal", Course_Category="Core")
        c3 = Course(Course_ID="COR003", Course_Name="Team Building", Course_Desc="Team Building", Course_Status="Pending", Course_Type="Internal", Course_Category="Core")
        
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()
        
        response = self.client.get("/api/course/Retired")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Course_List": [
                        {
                            "Course_ID": c2.Course_ID, 
                            "Course_Name": c2.Course_Name,
                            "Course_Desc": c2.Course_Desc,
                            "Course_Status": c2.Course_Status,
                            "Course_Type": c2.Course_Type,
                            "Course_Category": c2.Course_Category
                        }
                    ]
            }
        })
        
    def test_get_course_by_PendingStatus(self):
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR002", Course_Name="Effective Communication", Course_Desc="Effective Communication", Course_Status="Retired", Course_Type="Internal", Course_Category="Core")
        c3 = Course(Course_ID="COR003", Course_Name="Team Building", Course_Desc="Team Building", Course_Status="Pending", Course_Type="Internal", Course_Category="Core")
        
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()
        
        response = self.client.get("/api/course/Pending")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Course_List": [
                        {
                            "Course_ID": c3.Course_ID, 
                            "Course_Name": c3.Course_Name,
                            "Course_Desc": c3.Course_Desc,
                            "Course_Status": c3.Course_Status,
                            "Course_Type": c3.Course_Type,
                            "Course_Category": c3.Course_Category
                        }
                    ]
            }
        })
    
    def test_get_course_by_nonexistingstatus(self):
        response = self.client.get("/api/course/Wait")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no available course."
        }) 

"""
Registration 
- Get Course Registration by staffid
"""
class TestGetRegistrationByStaff(TestApp):
    def test_get_registration_by_staff(self):
        role1 = Role(Role_Name = "Admin")
        role2 = Role(Role_Name = "User")
        
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()
        
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="pehtingyu@gmail.com", Role=role1.Role_ID)
        st2 = Staff(Staff_FName='Evelyn', Staff_LName='Peh Ting Yu', Dept="Sales", Email="pehtingyu@gmail.com", Role=role2.Role_ID)

        db.session.add(st1)
        db.session.add(st2)
        db.session.commit()
        
        r1 = Registration(Course_ID="COR001", Staff_ID=st1.Staff_ID, Reg_Status="Registered", Completion_Status="Completed")
        r2 = Registration(Course_ID="COR002", Staff_ID=st2.Staff_ID, Reg_Status="Registered", Completion_Status="Completed")

        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        
        response = self.client.get("/api/registration/"+str(r1.Staff_ID))

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Registration_List": [
                        {
                            "Reg_ID": 1, 
                            "Course_ID": r1.Course_ID,
                            "Staff_ID": r1.Staff_ID,
                            "Reg_Status": r1.Reg_Status,
                            "Completion_Status": r1.Completion_Status
                        }
                    ]
            }
        })
        
    def test_get_registration_by_nonexistingstaff(self):
        response = self.client.get("/api/registration/100")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no registration"
        }) 

"""
Job Role
- Create Job Role
- Get Job Role by ID
- Get Job Role by Status
- View All Job Roles
- Update Job Role
"""

## Create Job Role
class TestCreateJobRole(TestApp):
    def test_create_JobRole(self):
        s1 = Skill(Skill_Name='Video Editing')
        s2 = Skill(Skill_Name='Photography')
        
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        request_body = {
            "Job_Role_Name": "Video Producer",
            "Job_Role_Desc": "Produce Weekly Video",
            "Job_Role_Skills": [s1.Skill_ID, s2.Skill_ID]
        }
        
        response = self.client.post("/api/jobrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        temp = json.loads((response.data).decode('utf-8'))
        #print(temp["data"]["Job_Role_ID"])
        
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "Job_Role_Desc": "Produce Weekly Video",
                "Job_Role_ID": temp["data"]["Job_Role_ID"],
                "Job_Role_Name": "Video Producer",
                "Job_Role_Status": "Active",
                "SkillList": [
                    {
                        "Job_Role_ID": temp["data"]["Job_Role_ID"],
                        "Skill_ID": s1.Skill_ID
                    },
                    {
                        "Job_Role_ID": temp["data"]["Job_Role_ID"],
                        "Skill_ID": s2.Skill_ID
                    }
                ]
            },
            "message": "Job Role has been successfully created!"
        })
        
    def test_create_existing_JobRole(self):
        s1 = Skill(Skill_Name='Video Editing')
        s2 = Skill(Skill_Name='Photography')
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(jr1)
        db.session.commit()
        
        request_body = {
            "Job_Role_Name": "Video Producer",
            "Job_Role_Desc": "Produce Weekly Video",
            "Job_Role_Skills": [s1.Skill_ID, s2.Skill_ID]
        }
        
        response = self.client.post("/api/jobrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
                   
        self.assertEqual(response.json, {
                        "code": 400,
                        "data": {
                            "Job_Role_Desc": "Produce Weekly Video",
                            "Job_Role_ID": jr1.Job_Role_ID,
                            "Job_Role_Name": "Video Producer",
                            "Job_Role_Status": "Active",
                            "SkillList": []
                        },
                        "message": "Job Role already existed"
                    })
    
# Get Job Role by ID
class TestGetJobRoleById(TestApp):
    def test_get_JobRole_by_id(self):
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        jr2 = JobRole(Job_Role_Name='Video Editor', Job_Role_Desc='Edit videos produced by producer')

        db.session.add(jr1)
        db.session.add(jr2)
        db.session.commit()
        
        response = self.client.get("/api/jobrole/"+ str(jr1.Job_Role_ID))

        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Job_Role_Desc":jr1.Job_Role_Desc,
                "Job_Role_ID": jr1.Job_Role_ID,
                "Job_Role_Name": jr1.Job_Role_Name,
                "Job_Role_Status": jr1.Job_Role_Status,
                "SkillList": []
            },
        })
        
    def test_get_JobRole_by_nonexistingid(self):
        
        response = self.client.get("/api/jobrole/100")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "No such jobrole record found"
        })

'''
class TestGetJobRoleByStatus(TestApp):
    def test_get_JobRole_by_ActiveStatus(self):
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        jr2 = JobRole(Job_Role_Name='Video Editor', Job_Role_Desc='Edit videos produced by producer')
        jr3 = JobRole(Job_Role_Name='Producer', Job_Role_Desc='Produce Video')
 
        db.session.add(jr1)
        db.session.add(jr2)
        db.session.add(jr3)
 
        db.session.commit()
        
        request_body = {
            "Job_Role_Name":"Producer",
            "Job_Role_Desc":"Produce Video",
            "Job_Role_Status": "Retired",
            "Job_Role_Dkills": []
        }
        
        self.client.put("/api/jobrole/"+ str(jr3.Job_Role_ID),
                            data=json.dumps(request_body),
                            content_type='application/json')
        
        
        response = self.client.get("/api/jobrole/Active")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Job_Role_List": [
                    {
                        "Job_Role_Desc": jr1.Job_Role_Desc,
                        "Job_Role_ID": jr1.Job_Role_ID,
                        "Job_Role_Name": jr1.Job_Role_Name,
                        "Job_Role_Status": jr1.Job_Role_Status,
                        "SkillList": []
                    },
                    {
                        "Job_Role_Desc": jr2.Job_Role_Desc,
                        "Job_Role_ID": jr2.Job_Role_ID,
                        "Job_Role_Name": jr2.Job_Role_Name,
                        "Job_Role_Status": jr2.Job_Role_Status,
                        "SkillList": []
                    },
                ]
            }
        })
        
    def test_get_JobRole_by_RetiredStatus(self):
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        jr2 = JobRole(Job_Role_Name='Video Editor', Job_Role_Desc='Edit videos produced by producer')
        jr3 = JobRole(Job_Role_Name='Producer', Job_Role_Desc='Produce Video')
 
        db.session.add(jr1)
        db.session.add(jr2)
        db.session.add(jr3)
 
        db.session.commit()
        
        request_body = {
            "Job_Role_Name":"Producer",
            "Job_Role_Desc":"Produce Video",
            "Job_Role_Status": "Retired",
            "Job_Role_Skills": []
        }
        
        self.client.put("/api/jobrole/"+ str(jr3.Job_Role_ID),
                            data=json.dumps(request_body),
                            content_type='application/json')
        
        
        response = self.client.get("/api/jobrole/Retired")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Job_Role_List": [
                    {
                        "Job_Role_Desc": jr3.Job_Role_Desc,
                        "Job_Role_ID": jr3.Job_Role_ID,
                        "Job_Role_Name": jr3.Job_Role_Name,
                        "Job_Role_Status": jr3.Job_Role_Status,
                        "SkillList": []
                    },
                ]
            }
        })
        
    def test_get_JobRole_by_nonexistingStatus(self):
        response = self.client.get("/api/jobrole/Pending")
        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no available Job Role."
        })
'''

class TestGetAllJobRole(TestApp):
    def test_get_all_JobRole(self):
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        jr2 = JobRole(Job_Role_Name='Video Editor', Job_Role_Desc='Edit videos produced by producer')

        db.session.add(jr1)
        db.session.add(jr2)
        db.session.commit()

        response = self.client.get("/api/jobrole")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Job_Role_List": [
                    {
                        "Job_Role_Desc": jr1.Job_Role_Desc,
                        "Job_Role_ID": jr1.Job_Role_ID,
                        "Job_Role_Name": jr1.Job_Role_Name,
                        "Job_Role_Status": jr1.Job_Role_Status,
                        "SkillList": []
                    },
                    {
                        "Job_Role_Desc": jr2.Job_Role_Desc,
                        "Job_Role_ID": jr2.Job_Role_ID,
                        "Job_Role_Name": jr2.Job_Role_Name,
                        "Job_Role_Status": jr2.Job_Role_Status,
                        "SkillList": []
                    }
                ]
            }
        })
        
    def test_NoJobRole(self):
        response = self.client.get("/api/jobrole")
        self.assertEqual(response.json, {
           "code": 404,
             "message": "There are no available Job Role."
        })

      
## Update Job Role
'''

class TestUpdateJobRole(TestApp):
    def test_update_jobrole(self):
        s1 = Skill(Skill_Name ="Leadership")        
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')

        db.session.add(jr1)
        db.session.add(s1)
        db.session.commit()
        
        request_body = {
            "Job_Role_Name":"Producer",
            "Job_Role_Desc":"Produce Video",
            "Job_Role_Status": "Retired",
            "Job_Role_Skills": [s1.Skill_ID]
        }
        
        response = self.client.put("/api/jobrole/"+ str(jr1.Job_Role_ID),
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                    "Job_Role_Desc": "Produce Video",
                    "Job_Role_ID": jr1.Job_Role_ID,
                    "Job_Role_Name": "Producer",
                    "Job_Role_Status": "Retired",
                    "SkillList": [
                        {
                        "Skill_ID": s1.Skill_ID,
                        "Job_Role_ID": jr1.Job_Role_ID
                    },
                    ]
                },
            "message": "Job Role has been successfully updated!"
        })
    
    def test_update_JobRole_by_nonexistingid(self):
        response = self.client.put("/api/jobrole/100")
        self.assertEqual(response.json, {
             "code": 404,
            "message": "No such job role record found."
        })

'''

"""
Skills
- Create Skill 
- Get Skills by ID
- Get Skills by Status (active and retired)
- Get All Skills 
- Update Skill by ID
""" 
 ## Create Skill
class TestCreateSkill(TestApp):
    def test_create_Skill(self):
        c1 = Course(Course_ID="COR100", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR200", Course_Name="Effective Communication", Course_Desc="Learn how to communicate effectively", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        request_body = {
            "Skill_Name":"Leadership",
            "Course_Skills": [c1.Course_ID, c2.Course_ID]
        }
        
        response = self.client.post("/api/skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        temp = json.loads((response.data).decode('utf-8'))
        
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "Skill_Name": "Leadership",
                "Skill_ID": temp["data"]["Skill_ID"],
                "Skill_Status": "Active",
                "Course_List": [
                    {
                        "Skill_ID": temp["data"]["Skill_ID"],
                        "Course_ID": c1.Course_ID
                    },
                    {
                        "Skill_ID": temp["data"]["Skill_ID"],
                        "Course_ID": c2.Course_ID
                    }
                ],
                "Job_List":[]
            },
            "message": "Skill has been successfully created!"
        })
        
    def test_create_existing_Skill(self):
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR002", Course_Name="Effective Communication", Course_Desc="Learn how to communicate effectively", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        s1 = Skill(Skill_Name ="Leadership")

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(s1)
        db.session.commit()
        
        request_body = {
            "Skill_Name":"Leadership",
            "Course_Skills": [c1.Course_ID, c2.Course_ID]
        }
        
        response = self.client.post("/api/skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
                   
        self.assertEqual(response.json, {
                            "code": 400,
                            "data": {
                                "Skill_Name": s1.Skill_Name
                            },
                            "message": "Skill already exists."
                        })  

## Get All Skills
class TestGetAllSkill(TestApp):
    def test_get_all_skill(self):
        s1 = Skill(Skill_Name='Video Editing')
        s2 = Skill(Skill_Name='Photography')

        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        response = self.client.get("/api/skill")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Skill_List": [
                    {
                        "Skill_ID": s1.Skill_ID,
                        "Skill_Name": s1.Skill_Name,
                        "Skill_Status": s1.Skill_Status,
                        "Course_List": [],
                        "Job_List": []
                    },
                    {
                        "Skill_ID": s2.Skill_ID,
                        "Skill_Name": s2.Skill_Name,
                        "Skill_Status": s2.Skill_Status,
                        "Course_List": [],
                        "Job_List": []
                    }
                ]
            }
        })
        
    def test_NoSkills(self):
        response = self.client.get("/api/skill")
        self.assertEqual(response.json, {
           "code": 404,
            "message": "There are no available skill."
        })

#Get Skills by ID
class TestGetSkillById(TestApp):
    def test_get_skill_by_id(self):
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        jr2 = JobRole(Job_Role_Name='Video Editor', Job_Role_Desc='Edit videos produced by producer')

        s1 = Skill(Skill_Name='Video Editing')
        s2 = Skill(Skill_Name='Photography')
        
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR002", Course_Name="Effective Communication", Course_Desc="Learn how to communicate effectively", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(jr1)
        db.session.add(jr2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        jrs1 = JobRoleSkill(Job_Role_ID= jr1.Job_Role_ID, Skill_ID=s1.Skill_ID)
        jrs2 = JobRoleSkill(Job_Role_ID= jr2.Job_Role_ID, Skill_ID=s1.Skill_ID)
        cs1 = CourseSkill(Course_ID = c1.Course_ID, Skill_ID=s1.Skill_ID)
        cs2 = CourseSkill(Course_ID=c2.Course_ID, Skill_ID=s1.Skill_ID)
        
        db.session.add(cs1)
        db.session.add(cs2)
        
        db.session.add(jrs1)
        db.session.add(jrs2)
        db.session.commit()
        
        response = self.client.get("/api/skill/"+ str(s1.Skill_ID))

        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Skill_Name": s1.Skill_Name,
                "Skill_ID": s1.Skill_ID,
                "Skill_Status": s1.Skill_Status,
                "Course_List": [
                    {
                        "Skill_ID": s1.Skill_ID,
                        "Course_ID": c1.Course_ID
                    },
                    {
                        "Skill_ID": s1.Skill_ID,
                        "Course_ID": c2.Course_ID
                    }
                ],
                "Job_List":[
                    {
                        "Skill_ID": s1.Skill_ID,
                        "Job_Role_ID": jr1.Job_Role_ID
                    },
                    {
                        "Skill_ID": s1.Skill_ID,
                        "Job_Role_ID": jr2.Job_Role_ID
                    }
                ]
            },
        })
        
    def test_get_skill_by_nonexistingid(self):
        response = self.client.get("/api/skill/100")
        self.assertEqual(response.json, {
           "code": 404,
            "message": "No such skill record found"
        })

#Get Skills by Status
class TestGetSkillByStatus(TestApp):
    def test_get_skill_by_ActiveStatus(self):
        s1 = Skill(Skill_Name='Video Editing')
        s2 = Skill(Skill_Name='Photography')
        s3 = Skill(Skill_Name='Production')
 
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
 
        db.session.commit()
        
        request_body = {
            "Skill_Name":"Photography",
            "Skill_Status": "Retired",
            "Course_Skills": []
        }
        
        self.client.put("/api/skill/"+ str(s3.Skill_ID),
                            data=json.dumps(request_body),
                            content_type='application/json')
        
        
        response = self.client.get("/api/skill/Active")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Skill_List": [
                    {
                        "Skill_ID": s1.Skill_ID,
                        "Skill_Name": s1.Skill_Name,
                        "Skill_Status": s1.Skill_Status,
                        "Course_List": [],
                        "Job_List": []
                    },
                    {
                        "Skill_ID": s2.Skill_ID,
                        "Skill_Name": s2.Skill_Name,
                        "Skill_Status": s2.Skill_Status,
                        "Course_List": [],
                        "Job_List": []
                    }
                ]
            }
        })
        
    def test_get_skill_by_RetiredStatus(self):
        s1 = Skill(Skill_Name='Video Editing')
        s2 = Skill(Skill_Name='Photography')
        s3 = Skill(Skill_Name='Production')
 
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
 
        db.session.commit()
        
        request_body = {
            "Skill_Name":"Photography",
            "Skill_Status": "Retired",
            "Course_Skills": []
        }
        
        self.client.put("/api/skill/"+ str(s3.Skill_ID),
                            data=json.dumps(request_body),
                            content_type='application/json')
        
        
        response = self.client.get("/api/skill/Retired")

        self.assertEqual(response.json, {
            "code": 200,
            "data":{
                "Skill_List": [
                    {
                        "Skill_ID": s3.Skill_ID,
                        "Skill_Name": s3.Skill_Name,
                        "Skill_Status": s3.Skill_Status,
                        "Course_List": [],
                        "Job_List": []
                    }
                ]
            }
        })
        
    def test_get_skill_by_nonexistingstatus(self):
        response = self.client.get("/api/skill/Pending")
        self.assertEqual(response.json, {
           "code": 404,
            "message": "There are no available skill."
        })


## Update Skills
class TestUpdateSkill(TestApp):
    def test_update_skill(self):
        s1 = Skill(Skill_Name ="Leadership")
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(s1)
        db.session.add(c1)
        db.session.commit()
        
        request_body = {
            "Skill_Name":"Leadership and Team Building",
            "Skill_Status": "Retired",
            "Course_Skills": [c1.Course_ID]
        }
        
        response = self.client.put("/api/skill/"+ str(s1.Skill_ID),
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                    "Skill_ID": s1.Skill_ID,
                    "Skill_Name": "Leadership and Team Building",
                    "Skill_Status": "Retired",
                    "Course_List": [
                            {
                                "Course_ID": c1.Course_ID,
                                "Skill_ID": s1.Skill_ID,
                            },
                        ],
                    "Job_List": []
                },
            "message": "Skill has been successfully updated!"
        })
    
    def test_update_Skill_by_nonexistingid(self):
        response = self.client.put("/api/skill/100")
        self.assertEqual(response.json, {
            "code": 404,
            "message": "No such skill record found."
        })

"""
Learning Journey 
- Create Learning Journey
- Get Learning Journey by Staff
- Get Learning Journey by Id
- Delete Learning Journey
"""
## Create Learning Journey
class TestCreateLearningJourney(TestApp):
    def test_create_LearningJourney(self):
        
        role1 = Role(Role_Name = "Admin")
        
        db.session.add(role1)
        db.session.commit()
        
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="pehtingyu@gmail.com", Role=role1.Role_ID)
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR002", Course_Name="Effective Communication", Course_Desc="Learn how to communicate effectively", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        
        db.session.add(jr1)
        db.session.add(st1)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        request_body = {
            "Staff_ID": st1.Staff_ID,
            "Job_Role_ID": jr1.Job_Role_ID,
            "Course_List": [c1.Course_ID, c2.Course_ID]
        }
        
        response = self.client.post("/api/learningjourney",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        temp = json.loads((response.data).decode('utf-8'))
        
        self.assertEqual(response.json, {
             "code": 201,
             "data": {
                    "CourseList": [
                    {
                        "Course_ID": c1.Course_ID,
                        "Learning_Journey_ID": temp["data"]["Learning_Journey_ID"]
                    },
                    {
                        "Course_ID": c2.Course_ID,
                        "Learning_Journey_ID": temp["data"]["Learning_Journey_ID"]
                    },
                ],
                "Job_Role_ID": 1,
                "Learning_Journey_ID": temp["data"]["Learning_Journey_ID"],
                "Staff_ID": st1.Staff_ID
                },
                "message": f'Learning Journey has been successfully created!'
            })  
        
        
## Get Learning Journey by Staff
class TestGetLearningJourneybyStaff(TestApp):
    def test_Get_LearningJourney_by_Staff(self):
        
        role1 = Role(Role_Name = "Admin")
        role2 = Role(Role_Name = "User")
        
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()
        
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="evelyn@gmail.com", Role=role1.Role_ID)
        st2 = Staff(Staff_FName='Evelyn', Staff_LName='Peh Ting Yu', Dept="Sales", Email="pehtingyu@gmail.com", Role=role2.Role_ID)
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(jr1)
        db.session.add(st1)
        db.session.add(st2)
        db.session.add(c1)
        db.session.commit()

        lj1 = LearningJourney(Staff_ID=st1.Staff_ID, Job_Role_ID=1)
        lj2 = LearningJourney(Staff_ID=st2.Staff_ID, Job_Role_ID=1)

        db.session.add(lj1)
        db.session.add(lj2)
        db.session.commit()
        
        lji1 = LearningJourneyItem(Learning_Journey_ID=lj1.Learning_Journey_ID, Course_ID=c1.Course_ID)
        db.session.add(lji1)
        db.session.commit()

        response = self.client.get("/api/learningjourney/"+str(st1.Staff_ID))
        
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                    "LearningJourney_List": [
                        {
                            "Learning_Journey_ID": lj1.Learning_Journey_ID,
                            "Staff_ID": st1.Staff_ID,
                            "Job_Role_ID": lj1.Job_Role_ID,
                            "CourseList": [
                                    {
                                        "Course_ID": lji1.Course_ID, 
                                        "Learning_Journey_ID": lj1.Learning_Journey_ID
                                    }
                            ]   
                        }
                    ]  
                }
            })  
        
    def test_Get_LearningJourney_by_nonexistingstaffid(self):
        response = self.client.get("/api/learningjourney/1")
        self.assertEqual(response.json, {
           "code": 404,
            "message": "No Available Learning Journey"
        })  


       
## Get Learning Journey by ID
class TestGetLearningJourneybyID(TestApp):
    def test_Get_LearningJourney_by_ID(self):
        role1 = Role(Role_Name = "Admin")
        db.session.add(role1)
        db.session.commit()
        
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="evelyn@gmail.com", Role=role1.Role_ID)
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(jr1)
        db.session.add(st1)
        db.session.add(c1)
        db.session.commit()

        lj1 = LearningJourney(Staff_ID=st1.Staff_ID, Job_Role_ID=1)

        db.session.add(lj1)
        db.session.commit()
        
        lji1 = LearningJourneyItem(Learning_Journey_ID=lj1.Learning_Journey_ID, Course_ID=c1.Course_ID)
        db.session.add(lji1)
        db.session.commit()

    
        response = self.client.get("/api/learningjourneybyid/"+str(lj1.Learning_Journey_ID))
        
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                    "Learning_Journey_ID": lj1.Learning_Journey_ID,
                    "Staff_ID": lj1.Staff_ID,
                    "Job_Role_ID": lj1.Job_Role_ID,
                    "CourseList": [
                        {
                            "Course_ID": lji1.Course_ID, 
                            "Learning_Journey_ID": lji1.Learning_Journey_ID
                        }
                    ]   
                }
            }) 
    
    def test_Get_LearningJourney_by_nonexistingid(self):
        response = self.client.get("/api/learningjourneybyid/1")
        self.assertEqual(response.json, {
           "code": 404,
            "message": "No such learning journey found"
        }) 

'''
## Delete Learning Journey by ID
class DeleteLearningJourneybyID(TestApp):
    def test_Delete_LearningJourney_by_ID(self):
        role1 = Role(Role_Name = "Admin")
        
        db.session.add(role1)
        db.session.commit()
    
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="evelyn@gmail.com", Role=role1.Role_ID)
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(jr1)
        db.session.add(st1)
        db.session.add(c1)
        db.session.commit()

        lj1 = LearningJourney(Staff_ID=st1.Staff_ID, Job_Role_ID=1)
        db.session.add(lj1)
        db.session.commit()
        
        lji1 = LearningJourneyItem(Learning_Journey_ID=lj1.Learning_Journey_ID, Course_ID=c1.Course_ID)
        db.session.add(lji1)
        db.session.commit()
      
        response = self.client.delete("/api/learningjourney/"+str(lj1.Learning_Journey_ID))
        
        self.assertEqual(response.json, {
                "code": 200,
                "message": "Learning Journey has been deleted successfully"
            }) 
        
    def test_Delete_LearningJourney_by_nonexistingID(self):
        
        response = self.client.delete("/api/learningjourney/100")
        
        self.assertEqual(response.json, {
                "code": 404,
                "message": "Learning Journey does not exist"
            }) 
'''        

"""
Learning Journey Item
- Create Learning Journey Item
- Delete Learning Journey Item
"""
#Create Learning Journey Item
class CreateLearningJourneyItem(TestApp):
    def test_Create_LearningJourneyItem(self):
        role1 = Role(Role_Name = "Admin")
        db.session.add(role1)
        db.session.commit()
        
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="evelyn@gmail.com", Role=role1.Role_ID)
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        c2 = Course(Course_ID="COR200", Course_Name="Effective Communication", Course_Desc="Learn how to communicate effectively", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(jr1)
        db.session.add(st1)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        lj1 = LearningJourney(Staff_ID=st1.Staff_ID, Job_Role_ID=1)
        db.session.add(lj1)
        db.session.commit()
        
        request_body = {
            "Course_List": [c1.Course_ID, c2.Course_ID]
        }
      
        response = self.client.post("/api/learningjourneyitem/"+str(lj1.Learning_Journey_ID),
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.json, {
                "code": 201,
                "message": f'Course(s) have been successfully added to selected learning journey!'
            }) 

## Delete Learning Journey Item by Course and LJ-ID
class DeleteLearningJourneyItem(TestApp):
    def test_Delete_LearningJourney_by_CourseandLJid(self):
        role1 = Role(Role_Name = "Admin")
        db.session.add(role1)
        db.session.commit()
        
        jr1 = JobRole(Job_Role_Name='Video Producer', Job_Role_Desc='Produce Weekly Video')
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="evelyn@gmail.com", Role=role1.Role_ID)
        c1 = Course(Course_ID="COR001", Course_Name="People Management", Course_Desc="Learn how to manage people", Course_Status="Active", Course_Type="Internal", Course_Category="Core")

        db.session.add(jr1)
        db.session.add(st1)
        db.session.add(c1)
        db.session.commit()

        lj1 = LearningJourney(Staff_ID=st1.Staff_ID, Job_Role_ID=1)
        db.session.add(lj1)
        db.session.commit()
        
        lji1 = LearningJourneyItem(Learning_Journey_ID=lj1.Learning_Journey_ID, Course_ID=c1.Course_ID)
        db.session.add(lji1)
        db.session.commit()
      
        response = self.client.delete("/api/learningjourneyitem/"+str(lj1.Learning_Journey_ID)+"/"+str(c1.Course_ID))
        
        self.assertEqual(response.json, {
               "code": 200,
                "message": "Course(s) have been successfully deleted to selected learning journey!"
            }) 
        
 

if __name__ == "__main__":
    unittest.main()
