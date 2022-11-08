<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>
    <div class="container-fluid">
        <div class="row" style="margin-top:100px">
            <h2 class="title">Choose Your Course</h2>
            <p class="title">You may click on the course name for more details of the course</p>
        </div>
        <div v-if="final_arr.length != 0">
            <div v-for="value, key in final_arr" :key="key" class="accordion" id="accordionExample">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingOne">
                    <button class="accordion-button" style="background-color:#80968a; color: white" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse'+key" aria-expanded="true" :aria-controls="'collapse'+key" >
                        {{value.Skill_Item.Skill_Name}}
                    </button>
                    </h2>
                    <div :id="'collapse'+key" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                        <div class="accordion-body">
                            <div v-if="(value.Course_List).length !=0">
                                <div v-for="course_value, course_key in value.Course_List" :key="course_key" class="form-check form-check-inline">
                                    <input class="form-check-input" type="checkbox" :id="course_value.Course_ID" :value="course_value.Course_ID" v-model="selected_course">
                                    <label class="form-check-label" @click="OpenModal(course_value)">{{course_value.Course_Name}}</label> 
                                    <span class="ms-1 badge" style="background-color:#80968a">{{course_value.registration_status}}</span>
                                </div>
                            </div>
                            <div v-else>
                                <h3> No Available Courses </h3>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </div>
            <div class="row" style="margin-top:20px">
                <div class="d-grid mb-2">
                <button type="button" class="btn btn-success p-2" @click="CreateLJ()">Create Learning Journey</button>
                </div>
            </div>
        </div>
        <div class="row mb-3 justify-content-center" v-else>
            <div class="col-sm-12 col-md-10">
                <div class="alert alert-danger show mb-5" role="alert">
                    <h4 class="text-center m-0">No Available Skills</h4>
                </div>
            </div>
        </div>
        
        
    </div>
</template>

<script>

import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";

export default {
    name: "CreateLearningJourney",
    components: { Loading, Modal },

    data() {
    return {
        //data preparation
        skills_arr : [],
        courses_arr: [],
        jobskills_arr: [],
        staff_registration_arr:[],
        final_arr: [],

        //selected course to add to learning journey
        selected_course:[],

        // Component item
        loading: null,
        modalMessage: null,
        modalActive: null,
        btnActive: true,
        }
    }, 

    created(){
        var selectedjobroleid = this.$route.params.jobroleid
        this.loading = true

        // Get All Staff's Registered Courses
        this.axios.get('http://localhost:5000/api/registration/'+this.$store.state.userid).then((response) => {
        this.staff_registration_arr = response.data.data.Registration_List
        console.log(this.staff_registration_arr)
        }).catch(error => {
            console.log(error)
        }).finally(() => {

            //Get All Active Courses
            this.axios.get('http://localhost:5000/api/course/Active').then((response) => {
            this.courses_arr = response.data.data.Course_List
            }).catch(error => {
                console.log(error)
            }).finally(() => {

                //Get All Active Skills
                this.axios.get('http://localhost:5000/api/skill/Active').then((response) => {
                this.skills_arr = response.data.data.Skill_List
                }).catch(error => {
                    console.log(error)
                }).finally(() => {

                    //Get Job Role Details
                    this.axios.get('http://localhost:5000/api/jobrole/'+ selectedjobroleid).then((response) => {
                        this.jobskills_arr = response.data.data.SkillList // retrieve the list of skills assigned to the job role
                    }).catch(error => {
                        console.log(error)
                    }).finally(() => {
                        //console.log(this.skills_arr)
                        //console.log(this.courses_arr)
                        //console.log(this.jobskills_arr)
                        for(var skill_item of this.skills_arr){ 
                            for(var sid of this.jobskills_arr){ //loop through the job role skillid and retrieve more details about the skills from the skills_arr
                                if(sid.Skill_ID == skill_item.Skill_ID){

                                    //each skill will have one json which consist of the skills and course details
                                    var json = {
                                        "Skill_Item": {"Skill_ID": skill_item.Skill_ID,"Skill_Name": skill_item.Skill_Name},
                                        "Course_List": []
                                    }

                                    var courses = skill_item.Course_List // retrieve the list of courseid under this skill
                                    for(var course_item of this.courses_arr){ //loop throuhgh the course id and retirve more details about the course from the course arr
                                        for(var cid of courses){
                                            if(course_item.Course_ID == cid.Course_ID){ 
                                                for(var r of this.staff_registration_arr){  //check if courses are registered
                                                    if(r.Course_ID == cid.Course_ID){  
                                                        var regi_status = r.Reg_Status
                                                        if (regi_status != "Rejected" & !this.selected_course.includes(r.Course_ID)){ //if registered or on waitlist, retrieve the reg_status and completion_status
                                                            
                                                            //this.selected_course.push(r.Course_ID) 
                                                            //course_item["disabled"] = true 

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
                                            }
                                        }
                                        
                                    }
                                    // after all courses has been added to the json then we add them to the final_arr for display
                                    this.final_arr.push(json)
                                }
                                
                            }
                        }    
                        //console.log(this.final_arr)
                        this.loading = false                
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
            this.$router.push({name:"ViewLearningJourney"})
        },
        CreateLJ(){
            if((this.selected_course).length!=0){
                this.loading = true;
     
                var json = {
                    "Staff_ID": this.$store.state.userid,  
                    "Job_Role_ID": this.$route.params.jobroleid,
                    "Course_List": this.selected_course,
                }
                this.axios.post('http://localhost:5000/api/learningjourney', json).then((response) => {
                    this.modalMessage = response.data.message + " Would you like to create another Learning Journey?"
                    this.btnActive = true
                    }).catch(error => {
                        this.modalMessage = error.response.data.message 
                        this.btnActive = false
                    }).finally(() => {
                        this.loading = false
                        this.modalActive = true; 
                    })
            }    
            else{
                this.modalActive = true
                this.modalMessage = "Please select a course"
                this.btnActive = false
            }
        }
               
    }
}
</script>

<style lang="scss" scoped>
h2 {
    margin: 0px !important;
}
.title {
    text-align: center;
}
.accordion-button::after {
    background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23ffffff'><path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/></svg>") !important;
 }

:focus {
  outline: 0 !important;
  box-shadow: 0 0 0 0 rgba(0, 0, 0, 0) !important;
}

</style>