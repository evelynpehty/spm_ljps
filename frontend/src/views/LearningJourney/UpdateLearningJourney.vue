<template>
<Loading v-show="loading" />
<Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>
    <div class="container-fluid">

        <div class="row" style="margin-top:80px">
            <h2 class="title">Update Learning Journey</h2>
            <p class="title">You may click on the course name for more details of the course</p>
        </div>

        <div v-if="final_arr.length != 0">
            <div v-for="value, key in final_arr" :key="key" class="accordion" id="accordionExample">
                <div v-if="(value.Course_List).length !=0" class="accordion-item">
                    <h2 class="accordion-header" id="headingOne">
                    <button class="accordion-button" style="background-color:#80968a; color: white" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse'+key" aria-expanded="true" :aria-controls="'collapse'+key" >
                        {{value.Skill_Item.Skill_Name}}
                    </button>
                    </h2>
                    <div :id="'collapse'+key" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                        <div class="accordion-body">  
                            <div v-for="course_value, course_key in value.Course_List" :key="course_key" class="form-check form-check-inline">
                                <input class="form-check-input" type="checkbox" :id="course_value.Course_ID" :value="course_value.Course_ID" v-model="selected_course">
                                <label class="form-check-label" @click="OpenModal(course_value)">{{course_value.Course_Name}}</label> 
                                <span class="ms-1 badge" style="background-color:#80968a">{{course_value.registration_status}}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-else>
              <h3> No Available Skills </h3>
        </div>

        <div v-if="retired_course_skills.length != 0">
            <div class="accordion" id="accordionExample">
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingOne">
                        <button class="accordion-button" style="background-color:#80968a; color: white" type="button"  data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            Courses that are retired or with no skill assigned
                        </button>
                        </h2>
                        <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                            <div class="accordion-body">   
                                <div v-for="value, key in retired_course_skills" :key="key" class="form-check form-check-inline">
                                    <input class="form-check-input" type="checkbox" :id="value.Course_ID" :value="value.Course_ID" v-model="selected_course">
                                    <label class="form-check-label" @click="OpenModal(value)">{{value.Course_Name}}</label> 
                                    <span class="ms-1 badge" style="background-color:#80968a">{{value.registration_status}}</span>
                                </div>
                            </div>
                        </div>
                    </div>
             </div>
        </div>
            
        <div class="row" style="margin-top:20px">
            <div class="d-grid mb-2">
                <button type="button" class="btn btn-success p-2" :disabled="enablebutton == true" @click="UpdateLJ()">Update Learning Journey</button>
            </div>
        </div>
    </div>
  </template>
  
  <script>
  
  import Loading from "/src/components/Loading";
  import Modal from "/src/components/Modal";
  
  export default {
      name: "UpdateLearningJourney",
      components: { Loading, Modal },
  
      data() {
      return {
          //data preparation
          learningjourney: null,
          existing_courseid_arr:[], //to keep a copy of originally selected courseid
          all_courses_arr: [],
          all_skills_arr: [],
          jobskills_arr: [],
          staff_registration_arr:[],
          retired_course_skills: [],

          active_courseid: [],
          retired_courseid: [],
          final_arr: [],
  
          selected_course:[],
          
          // Component item
          loading: null,
          modalMessage: null,
          modalActive: null,
          btnActive: false,
        }
      }, 
  
      created(){
        var selectedlearningjourney = this.$route.params.learningjourneyid
        this.loading = true

        // get learning journey by id
        this.axios.get('http://localhost:5000/api/learningjourneybyid/'+selectedlearningjourney).then((response) => {
        this.learningjourney = response.data.data

        for(var existingcourseitem of this.learningjourney.CourseList){
            this.existing_courseid_arr.push(existingcourseitem.Course_ID) //to keep a copy of originally selected courseid
            this.selected_course.push(existingcourseitem.Course_ID) //so that all the previously selected courseid will be selected   
        }

        }).catch(error => {
            this.loading = false
            this.modalMessage = error.response.data.message
            this.modalActive = true
        }).finally(() => {
            //get all courses
            this.axios.get('http://localhost:5000/api/course').then((response) => {
              this.all_courses_arr = response.data.data.Course_List
              }).catch(error => {
                this.loading = false
                this.modalMessage = error.response.data.message
                this.modalActive = true
              }).finally(() => {
                //get all skills
                this.axios.get('http://localhost:5000/api/skill').then((response) => {
                  this.all_skills_arr = response.data.data.Skill_List
                  }).catch(error => {
                    this.loading = false
                    this.modalMessage = error.response.data.message
                    this.modalActive = true
                  }).finally(() => {
                    // Get All Staff's Registered Courses
                    this.axios.get('http://localhost:5000/api/registration/'+this.$store.state.userid).then((response) => {
                    this.staff_registration_arr = response.data.data.Registration_List
                    }).catch(error => {
                        this.loading = false
                        this.modalMessage = error.response.data.message
                        this.modalActive = true
                    }).finally(() => {
                        //Get Job Role Details
                        this.axios.get('http://localhost:5000/api/jobrole/'+ this.learningjourney.Job_Role_ID).then((response) => {
                            this.jobskills_arr = response.data.data.SkillList // retrieve the list of skills assigned to the job role
                        }).catch(error => {
                            this.loading = false
                            this.modalMessage = error.response.data.message
                            this.modalActive = true
                        }).finally(() => {
                            for(var skill_item of this.all_skills_arr){ 
                                for(var sid of this.jobskills_arr){ //loop through the job role skillid and retrieve more details about the skills from the skills_arr
                                    if(sid.Skill_ID == skill_item.Skill_ID){
                                        var courses = skill_item.Course_List // retrieve the list of courseid under this skill
                                        //each skill will have one json which consist of the skills and course details
                                        if(skill_item.Skill_Status == "Active"){
                                        
                                            var json = {
                                                "Skill_Item": {"Skill_ID": skill_item.Skill_ID,"Skill_Name": skill_item.Skill_Name},
                                                "Course_List": []
                                            }  
                                            for(var course_item of this.all_courses_arr){ //loop through the course id and retrieve more details about the course from the course arr
                                                for(var cid of courses){
                                                    if(course_item.Course_ID == cid.Course_ID){ 
                                                        //console.log(course_item)
                                                        if(course_item.Course_Status == "Active"){
                                                            this.active_courseid.push(cid.Course_ID)
                                                            for(var r of this.staff_registration_arr){  //check if courses are registered
                                                                if(r.Course_ID == cid.Course_ID){  
                                                                    var regi_status = r.Reg_Status
                                                                    if (regi_status != "Rejected"){ //if registered or on waitlist, retrieve the reg_status and completion_status       
                                                                        var completion_status = r.Completion_Status //concat regstatus and completion status together to display in badge
                                                                        var text = regi_status
                                                                        if(completion_status != null){
                                                                            text = text + " - "  + completion_status 
                                                                        }
                                                                        course_item["registration_status"] = text
                                                                    }
                                                                    
                                                                }
                                                            }
                                                           
                                                            json["Course_List"].push(course_item)
                                                            //console.log(course_item)
                                                            
                                                        }
                                                    
                                                        //console.log(this.existing_courseid_arr)
                                                        if((this.existing_courseid_arr).includes(course_item.Course_ID) & course_item.Course_Status != "Active"){
                                                            (this.retired_course_skills).push(course_item)
                                                            //console.log(this.retired_course_skills)
                                                        }
                                                        
                                                    }
                                                }
                                            }
                                            this.final_arr.push(json)
                                            //console.log(this.final_arr)
                                        }
                                        // if skills status = retired, set all courses under it as inactive
                                        else{
                                            for(var r_cid of courses){                                                    
                                                (this.retired_courseid).push(r_cid.Course_ID)
                                                for(var r_ci of this.all_courses_arr){ //loop through the course id and retrieve more details about the course from the course arr
                                                    if(r_ci.Course_ID == r_cid.Course_ID){
                                                        if((this.existing_courseid_arr).includes(r_ci.Course_ID)){
                                                            for(var r2 of this.staff_registration_arr){  //check if courses are registered
                                                                if(r2.Course_ID == r_cid.Course_ID){  
                                                                    if (r2.Reg_Status != "Rejected"){ //if registered or on waitlist, retrieve the reg_status and completion_status       
                                                                        var completion_status2 = r2.Completion_Status //concat regstatus and completion status together to display in badge
                                                                        var text2 = r2.Reg_Status
                                                                        if(completion_status2 != null){
                                                                            text2 = text2 + " - "  + completion_status2 
                                                                        }
                                                                        r_ci["registration_status"] = text2
                                                                    }
                                                                    
                                                                }
                                                            }
                                                            (this.retired_course_skills).push(r_ci)
                                                            
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }                                
                            }   

                            var common = (this.retired_courseid).filter(element => this.active_courseid.includes(element));                         
                            for(var com of common){
                                for(var rcid in this.retired_course_skills){
                                    if(this.retired_course_skills[rcid].Course_ID == com){
                                        (this.retired_course_skills).splice(rcid,1)
                                    }
                                }
                            }

                            this.loading = false   
                        })
                    })
                })
            })
        })
      },
      methods:{
          closeModal() {
              this.modalActive = !this.modalActive;
          },
          OpenModal(course_value){
              this.modalActive = true
              this.btnActive = false
              this.modalMessage = course_value.Course_Desc
          },
          btnYes() {
              this.$router.push({name:"SelectJobRole"})
          },
  
          btnNo(){
              this.$router.push({name:"ManageLearningJourney"})
          },
          arrayEquals(a, b) {
                return Array.isArray(a) &&
                    Array.isArray(b) &&
                    a.length === b.length &&
                    a.every((val, index) => val === b[index]);
          },
          UpdateLJ(){
            if((this.selected_course).length != 0){
                var add_item = this.selected_course.filter(x => !this.existing_courseid_arr.includes(x));
                console.log(add_item)

                var delete_item = this.existing_courseid_arr.filter(x => !this.selected_course.includes(x));
                console.log(delete_item)

                
                var add_json = {
                    "Course_List": add_item
                }

                var delete_json = {
                    "Course_List": delete_item
                }

                if(add_item.length != 0){
                    this.axios.post('http://localhost:5000/api/learningjourney'+this.$route.params.learningjourneyid, add_json).then((response) => {
                    this.modalMessage = response.data.message
                    }).catch(error => {
                        this.modalMessage = error.response.data.message 
                        this.btnActive = false
                    }).finally(() => {
                        this.loading = false
                        this.modalActive = true; 
                    })
                }

                if(delete_item.length != 0){
                    this.axios.delete('http://localhost:5000/api/learningjourney'+this.$route.params.learningjourneyid, delete_json).then((response) => {
                    this.modalMessage = response.data.message
                    }).catch(error => {
                        this.modalMessage = error.response.data.message 
                        this.btnActive = false
                    }).finally(() => {
                        this.loading = false
                        this.modalActive = true; 
                    })
                }

            }

            else{
                this.modalActive = true
                this.modalMessage = "Please select a course"
                this.btnActive = false
            }
             
          }
                 
      },
      computed: {
        enablebutton(){
            if(this.arrayEquals(this.selected_course, this.existing_courseid_arr)){
                return true
            }
            return false
        }
    
    }
  }
  </script>
  
  <style>
  .accordion-button::after {
      background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23ffffff'><path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/></svg>") !important;
   }
  
  :focus {
    outline: 0 !important;
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0) !important;
  }
  
  </style>                       


