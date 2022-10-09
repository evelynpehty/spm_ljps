<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>
    <div class="container-fluid">
        <div class="row" style="margin-top:80px">
            <h2 class="title">Choose Your Course</h2>
            <p class="title">You may click on the course name for more details of the course</p>
            
        </div>
        <div v-for="value, key in final_arr" :key="key" class="accordion" id="accordionExample">
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingOne">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse'+key" aria-expanded="true" :aria-controls="'collapse'+key">
                    {{value.Skill_Item.Skill_Name}}
                </button>
                </h2>
                <div :id="'collapse'+key" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                    <div v-for="course_value, course_key in value.Course_List" :key="course_key" class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" :id="course_value.Course_ID" :value="course_value.Course_ID" v-model="selected_course">
                        <label class="form-check-label" @click="OpenModal(course_value)">{{course_value.Course_Name}}</label>
                    </div>
                </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="d-grid mb-2">
               <button type="button" class="btn btn-success p-2" @click="CreateLJ()">Create Learning Journey</button>
            </div>
        </div>
    </div>
</template>

<script>

import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";

export default {
    name: "SelectJobRolesPage",
    components: { Loading, Modal },

    data() {
    return {
        //data preparation
        skills_arr : [],
        courses_arr: [],
        jobskills_arr: [],
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

        this.axios.get('http://localhost:5000/api/course/Active').then((response) => {
        this.courses_arr = response.data.data.Course_List
        }).catch(error => {
            console.log(error)
        }).finally(() => {

            this.axios.get('http://localhost:5000/api/skill/Active').then((response) => {
            this.skills_arr = response.data.data.Skill_List
            }).catch(error => {
                console.log(error)
            }).finally(() => {

                this.axios.get('http://localhost:5000/api/jobrole/'+ selectedjobroleid).then((response) => {
                    this.jobskills_arr = response.data.data.SkillList
                }).catch(error => {
                    console.log(error)
                }).finally(() => {
                    //console.log(this.skills_arr)
                    //console.log(this.courses_arr)
                    //console.log(this.jobskills_arr)
                    for(var skill_item of this.skills_arr){
                        for(var sid of this.jobskills_arr){
                            if(sid.Skill_ID == skill_item.Skill_ID){
                                console.log(sid)
                                var json = {
                                    "Skill_Item": {"Skill_ID": skill_item.Skill_ID,"Skill_Name": skill_item.Skill_Name},
                                    "Course_List": []
                                }
                                var courses = skill_item.Course_List
                                for(var course_item of this.courses_arr){
                                    for(var cid of courses){
                                        if(course_item.Course_ID == cid.Course_ID){
                                            //this.final_arr[sid.Skill_Name].push(course_item)
                                            json["Course_List"].push(course_item)
                                        }
                                    }
                                    
                                }
                                this.final_arr.push(json)

                            }
                            
                        }
                    }    
                    console.log(this.final_arr)
                    this.loading = false                
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

<style>

</style>