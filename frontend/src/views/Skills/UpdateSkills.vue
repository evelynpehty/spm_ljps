<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>
  
    <div class="container-fluid">
      <div class="row" style="margin-top:80px">
        <h2 class="title">Update Skill</h2>
        <p class="title">Please fill in all required fields to successfully update this selected skill.</p>
      </div>
      <br>
  
      <div v-if="errors.length != 0">
        <div class="alert alert-danger show mb-5" role="alert">
          <h4>Please check your inputs</h4>
          <ul>
            <li class="m-0" v-for="e in errors" :key="e">{{e}}</li>
          </ul>
        </div>
      </div>
  
      <div v-if="warnings.length != 0">
        <div class="alert alert-warning show mb-5" role="alert">
          <h4>Please check your inputs</h4>
          <ul>
            <li class="m-0" v-for="w in warnings" :key="w">{{w}}</li>
          </ul>
        </div>
      </div>
  
      <div class="card border-0 shadow p-3 mb-5 bg-white rounded">
        <div class="card-body">
          <form @submit.prevent v-on:submit="checkForm">
            <div class="row mb-3">
              <div class="col-md-8">
                <label for="SkillName" class="form-label">Skill Name</label>
                <input type="text" class="form-control form-control-md input-border-color" id="SkillName" placeholder="e.g. Python Programming" v-model="SkillName">
              </div>
              <div class="col-md-4">
                <label for="SkillName" class="form-label">Skill Status</label>
                <div class="mt-2">
                  <span class="me-2">Inactive</span>
                  <Toggle v-model="value" />
                  <span class="ms-2">Active</span>
                </div>
              </div>

            </div>

            <div v-if="boolCourses" class="mb-3">
              <label for="CourseName" class="form-label">Course affiliated with Skill</label>
              <VueMultiselect
              :preserve-search="true"
              :multiple="true"
              :close-on-select="false"
              :options="activeCourses"
              v-model="selectedCourses"
              label="Course_Name"
              track-by="Course_Name"
              placeholder="Select Courses..."
              />
            </div>
            <div v-else class="mb-3">
              <label for="CourseName" class="form-label">Course affiliated with Skill</label>
              <VueMultiselect
              :preserve-search="true"
              :multiple="true"
              :close-on-select="false"
              :options="activeCourses"
              v-model="selectedCourses"
              label="Course_Name"
              track-by="Course_Name"
              placeholder="No Available Course..."
              />
            </div>
  
            <div class="d-grid mb-2">
              <button v-if="changes" type="submit" class="btn btn-success p-2">Update</button>
              <button v-else type="submit" class="btn btn-success p-2" disabled>Update</button>
            </div>
        </form>
        </div>
      </div>    
    </div>
  </template>
  
  <script>
  import Modal from "/src/components/Modal";
  import Loading from "/src/components/Loading";
  import VueMultiselect from 'vue-multiselect';
  import Toggle from '@vueform/toggle'

  export default {
    name: "UpdateSkills",
  
    components: {
      Modal,
      Loading,
      VueMultiselect,
      Toggle
    },
  
    data () {
      return {
        // Skills Details
        skillID : this.$route.params.skillID,
        SkillName : "",
        SkillStatus : "",

        // Courses
        CourseList : [],
        tempCourseList : [],
        selectedCourses : [],
        tempActiveCourses : [],
        activeCourses : [],
        boolCourses : true,

        // Comparison - Store Previous Values
        SkillName_Copy: "",
        SkillStatus_Copy: "",
        CourseList_Copy: "",
        selectedCourses_copy : [],
        value_copy : null,

        // Component item
        loading: null,
        modalMessage: "Skills Updated Successfully. Would you like to update again?",
        modalActive: null,
        btnActive: true,
        value: null,
      
        // Errors
        errors: [],
  
        // Warnings
        warnings: []
      }
    },
    created() {
      this.loading = true

      this.axios.get("http://127.0.0.1:5000/api/skill/" + this.skillID).then((response) => {
        var apiData = response.data.data

        this.SkillName = apiData.Skill_Name
        this.SkillStatus = apiData.Skill_Status
        this.CourseList = apiData.Course_List

        // Storing for Comparison
        this.SkillName_Copy = apiData.Skill_Name
        this.SkillStatus_Copy = apiData.Skill_Status
        this.CourseList_Copy = apiData.Course_List

        if (this.SkillStatus == "Active") {
          this.value = true
          this.value_copy = true
        } else {
          this.value = false
          this.value_copy = false
        }

        for ( var i in this.CourseList ) {
          this.tempCourseList.push(this.axios.get("http://127.0.0.1:5000/api/course/id/" + this.CourseList[i].Course_ID))
        }

        this.tempActiveCourses = this.axios.get("http://localhost:5000/api/course/Active")
      }).catch(error => {
        if (error.response.data.code == "404"){
                this.error = error.response.data.message
            } else {
                this.error = "Error occured in retrieving Skills Data"
            }
      }).finally(() => {
        Promise.all(this.tempCourseList).then((responses) => {
          for (var r in responses) {
            this.CourseList[r]["Course_Name"] = responses[r].data.data.Course_Name 
          }
        }).finally(() => {
          Promise.all([this.tempActiveCourses]).then((responses) => {
            this.tempActiveCourses = responses[0].data.data.Course_List
          }).finally(() => {
            this.selectedCourses_copy = this.CourseList
            this.selectedCourses = this.CourseList
            this.activeCourses = this.tempActiveCourses
            this.loading = false
          })
        })
      })
    }, 

    computed: {
      changes() {
        if ( this.value_copy != this.value | this.SkillName_Copy != this.SkillName | this.arrayEquals(this.selectedCourses_copy, this.selectedCourses) ) {
          return true
        } else {
          return false
        }
        
      }
    },

    methods: {
      
      closeModal() {
        this.modalActive = !this.modalActive;
      },
  
      btnYes() {
        this.closeModal()
        this.$router.go(this.$router.currentRoute)
      },
  
      btnNo(){
        this.$router.push({name:"ViewAllSkills"})
      },
  
      checkForm(){
        this.errors = [];
        this.warnings = [];
  
        if (this.SkillName.trim().length == 0) {
          this.errors.push("Skill Name is empty! Please enter  Skill Name.")
        }
  
        if (this.selectedCourses.length == 0) {
          this.errors.push("No Courses selected! Please select at least 1 course.")
        }
  
        if (this.SkillName.length > 50) {
          this.warnings.push("Skill Name is too long! It should not exceed 50 characters. Please try again!")
        }
  
        if (this.errors.length == 0 && this.warnings.length == 0) {
          this.UpdateSkill()
        }
      },
  
      resetField() {
        this.SkillName = "";
        this.selectedCourses = []
      },
  
      UpdateSkill() {
        var selected_courseid = []
        for(var c of this.selectedCourses){
          selected_courseid.push(c.Course_ID)
        }
        this.loading = true;
       
        if (this.value == true) {
          this.SkillStatus = "Active"
        } else {
          this.SkillStatus = "Retired"
        }

        var json = {
          "Skill_Name": this.SkillName,  
          "Skill_Status" : this.SkillStatus,
          "Course_Skills": selected_courseid,
        }
        this.axios.put('http://localhost:5000/api/skill/' + this.skillID, json).then((response) => {
            this.modalMessage = response.data.message + " Would you like to update again?"
            this.btnActive = true
          }).catch(error => {
              this.modalMessage = error.response.data.message 
              this.btnActive = false
          }).finally(() => {
              this.loading = false
              this.modalActive = true; 
          })
      },

      arrayEquals(a, b) {
        var difference = a
          .filter(x => !b.includes(x))
          .concat(b.filter(x => !a.includes(x)));            

        if(difference.length == 0){
            return false
        }
        else{
            return true
        }
      }
  
    }
  
  }
  </script>
  <style src="@vueform/toggle/themes/default.css"></style>
  <style lang="scss" scoped>
  h2 {
     margin: 0px !important;
  }
  
  .title {
    text-align: center;
  }
  </style>
  