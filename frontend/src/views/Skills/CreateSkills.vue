<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">Create Skills</h2>
      <p class="title">Please fill in the required fields to successfully create a skills.</p>
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
          <div class="mb-3">
            <label for="SkillName" class="form-label">Skill Name</label>
            <input type="text" class="form-control form-control-md input-border-color" id="SkillName" placeholder="e.g. Python Programming" v-model="SkillName">
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
            <button type="submit" class="btn btn-success p-2">Create</button>
          </div>
      </form>
      </div>
    </div>    
  </div>
</template>

<script>
import Modal from "/src/components/Modal";
import Loading from "/src/components/Loading";
import VueMultiselect from 'vue-multiselect'

export default {
  name: "CreateSkills",

  components: {
    Modal,
    Loading,
    VueMultiselect
  },

  data () {
    return {
      // Course Information
      SkillName : "",

      // Courses
      activeCourses : [],
      boolCourses : true,
      selectedCourses:[],

      // Component item
      loading: null,
      modalMessage: "Skills Created Successfully. Would you like to create another Course?",
      modalActive: null,
      btnActive: true,
    
      // Errors
      errors: [],

      // Warnings
      warnings: []
    }
  },
  created() {
    this.loading = true
    this.axios.get("http://localhost:5000/api/course/Active").then((response)=> {
      console.log(response.data.data)
      this.activeCourses = response.data.data.Course_List
    }).catch(error => {
      console.log(error.response.data)
      if (error.response.data.code == "404") {
        this.boolCourses = false
      }
    }).finally(() => {
      this.loading = false
    })
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

      console.log(this.errors);

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
        this.CreateSkill()
      }
    },

    resetField() {
      this.SkillName = "";
      this.selectedCourses = []
    },

    CreateSkill() {
      var selected_courseid = []
      for(var c of this.selectedCourses){
        selected_courseid.push(c.Course_ID)
      }
      this.loading = true;
     
      var json = {
        "Skill_Name": this.SkillName,  
        "Course_Skills": selected_courseid,
      }
      this.axios.post('http://localhost:5000/api/skill', json).then((response) => {
          this.modalMessage = response.data.message + " Would you like to create another Skill?"
          this.btnActive = true
        }).catch(error => {
            this.modalMessage = error.response.data.message 
            this.btnActive = false
        }).finally(() => {
            this.loading = false
            this.modalActive = true; 
        })
    }

  }

}
</script>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>
<style lang="scss" scoped>
h2 {
   margin: 0px !important;
}

.title {
  text-align: center;
}
</style>
