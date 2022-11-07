import unittest

from models import Role, Staff, Course, Registration, JobRole, Skill, JobRoleSkill, CourseSkill, LearningJourney, LearningJourneyItem

class TestRole(unittest.TestCase):
    def test_to_dict(self):
        r1 = Role(Role_Name = "Admin")
        self.assertEqual(r1.json(), {
            "Role_ID": r1.Role_ID,
            "Role_Name": "Admin"
        })

class TestStaff(unittest.TestCase):
    def test_to_dict(self):
        st1 = Staff(Staff_FName='Peh', Staff_LName='Ting Yu', Dept="Human Resource", Email="pehtingyu@gmail.com", Role=1)
        self.assertEqual(st1.json(), {
            "Staff_ID": st1.Staff_ID, 
            "Staff_FName": "Peh",
            "Staff_LName": "Ting Yu",
            "Email": "pehtingyu@gmail.com",
            "Dept": "Human Resource",
            "Role": 1,
        })

class TestCourse(unittest.TestCase):
    def test_to_dict(self):
        c1 = Course(Course_ID="COR001", Course_Name="System Thinking", Course_Desc="Think About System", Course_Status="Active", Course_Type="Internal", Course_Category="Core")
        self.assertEqual(c1.json(), {
            "Course_ID": "COR001",
            "Course_Name": "System Thinking",
            "Course_Desc": "Think About System",
            "Course_Status": "Active",
            "Course_Type": "Internal",
            "Course_Category": "Core"
        })

class TestRegistration(unittest.TestCase):
    def test_to_dict(self):
        r1 = Registration(Course_ID="COR001", Staff_ID=140001, Reg_Status="Registered", Completion_Status="Completed")
        self.assertEqual(r1.json(), {
            "Reg_ID": r1.Reg_ID,
            "Course_ID": "COR001",
          "Staff_ID": 140001,
            "Reg_Status": "Registered",
            "Completion_Status": "Completed"
        })

class TestJobRole(unittest.TestCase):
    def test_to_dict(self):
        jr1 = JobRole(Job_Role_Name='Frontend', Job_Role_Desc='Build Frontend Application')
        self.assertEqual(jr1.json(), {
            "Job_Role_ID": jr1.Job_Role_ID,
            "Job_Role_Name": "Frontend",
            "Job_Role_Desc": "Build Frontend Application",
            "Job_Role_Status": None,
            "SkillList": []
        })
        
class TestJobRoleSkill(unittest.TestCase):
    def test_to_dict(self):
        jrs1 = JobRoleSkill(Job_Role_ID=1, Skill_ID=1)
        self.assertEqual(jrs1.json(), {
            "Skill_ID": 1,
            "Job_Role_ID": 1,
        })        
        
class TestSkill(unittest.TestCase):
    def test_to_dict(self):
        s1 = Skill(Skill_Name='Vue')
        self.assertEqual(s1.json(), {
            "Skill_ID": s1.Skill_ID,
            "Skill_Name": "Vue",
            "Skill_Status": None,
            "Job_List": [],
            "Course_List": []
        })
        
class TestCourseSkill(unittest.TestCase):
    def test_to_dict(self):
        cs1 = CourseSkill(Course_ID="COR001", Skill_ID=1)
        self.assertEqual(cs1.json(), {
            "Skill_ID": 1,
            "Course_ID": "COR001",
        })    
        
class TestLearningJourney(unittest.TestCase):
    def test_to_dict(self):
        lj1 = LearningJourney(Staff_ID=140001, Job_Role_ID=1)
        self.assertEqual(lj1.json(), {
            "Learning_Journey_ID": lj1.Learning_Journey_ID,
            "Staff_ID": 140001,
            "Job_Role_ID": 1,
            "CourseList": []
        })
        
class TestLearningJourneyItem(unittest.TestCase):
    def test_to_dict(self):
        lji1 = LearningJourneyItem(Learning_Journey_ID=1, Course_ID="COR001")
        self.assertEqual(lji1.json(), {
            "Learning_Journey_ID": 1,
            "Course_ID": "COR001",
        })

if __name__ == "__main__":
    unittest.main()
