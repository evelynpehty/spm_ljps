<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">Create Job Role</h2>
      <p class="title">Please fill in the required fields to successfully create a job role.</p>
    </div>
    <br>

    <div v-if="errors.length != 0">
      <div class="alert alert-danger alert-dismissible fade show mb-5" role="alert">
        <h4>Please check your inputs</h4>
        <ul>
          <li class="m-0" v-for="e in errors" :key="e">{{e}}</li>
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    </div>

    <div v-if="warnings.length != 0">
      <div class="alert alert-warning alert-dismissible fade show mb-5" role="alert">
        <h4>Please check your inputs</h4>
        <ul>
          <li class="m-0" v-for="w in warnings" :key="w">{{w}}</li>
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    </div>

    <div class="card border-0 shadow p-3 mb-5 bg-white rounded">
      <div class="card-body">
        <form @submit.prevent v-on:submit="checkForm">
          <div class="mb-3">
            <label for="JobRoleName" class="form-label">Job Role Name</label>
            <input type="text" class="form-control form-control-md input-border-color" id="JobRoleName" placeholder="e.g. Software Engineer" v-model="JobRoleName">
          </div>

          <div class="mb-3">
            <label for="JobRoleDesc" class="form-label">Job Role Description</label>
            <textarea class="form-control form-control-md input-border-color" placeholder="e.g. Will be tasked to code the frontend of application." id="floatingTextarea" style="height: 100px;" v-model="JobRoleDesc"></textarea>
          </div>

          <div v-if="boolSkills" class="mb-3">
            <label for="SkillName" class="form-label">Skills affiliated with Job Role</label>
            <VueMultiselect
            :preserve-search="true"
            :multiple="true"
            :close-on-select="false"
            :options="activeSkills"
            v-model="selectedSkills"
            label="Skill_Name"
            track-by="Skill_Name"
            placeholder="Select Skills..."
            />
          </div>
          <div v-else class="mb-3">
            <label for="SkillName" class="form-label">Skills affiliated with Job Role</label>
            <VueMultiselect
            :preserve-search="true"
            :multiple="true"
            :close-on-select="false"
            :options="activeSkills"
            v-model="selectedSkills"
            label="Skill_Name"
            track-by="Skill_Name"
            placeholder="No Available Skills..."
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
  name: "CreateJobs",

  components: {
    Modal,
    Loading,
    VueMultiselect
  },

  data () {
    return {
      // Job Role Information
      JobRoleName : "",
      JobRoleDesc : "",

      // Skills
      activeSkills : [],
      boolSkills : true,
      selectedSkills :[],


      // Component item
      loading: null,
      modalMessage: "Job Created Successfully. Would you like to create another job role?",
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
    this.axios.get("http://localhost:5000/api/skill/Active").then((response)=> {
      this.activeSkills = response.data.data.Skill_List
      console.log(this.activeSkills)
    }).catch(error => {
      console.log(error.response.data)
      if (error.response.data.code == "404") {
        this.boolSkills = false
        console.log(this.activeSkills)
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
      this.$router.push({name:"ViewAllJobs"})
    },

    checkForm(){
      this.errors = [];
      this.warnings = [];

      if (this.JobRoleName.trim().length == 0) {
        this.errors.push("Job Role Name is empty! Please enter Job Role Name.")
      }

      if (this.JobRoleDesc.trim().length == 0) {
        this.errors.push("Job Role Description is empty! Please enter Job Role Description.")
      }

      if (this.selectedSkills.length == 0) {
        this.errors.push("No Skills selected! Please select at least 1 skill.")
      }

      if (this.JobRoleDesc.length > 255) {
        this.warnings.push("Job Description is too long! It should not exceed 255 characters. Please try again!")
      }
      console.log(this.warnings)

      if (this.errors.length == 0) {
        this.CreateJobRole()
      }
    },

    resetField() {
      this.JobRoleName = "";
      this.JobRoleDesc = "";
      this.SelectedSkills = ""
    },

    CreateJobRole() {
      var selected_skillid = []
      for(var j of this.selectedSkills){
        selected_skillid.push(j.Skill_ID)
      }
      this.loading = true;
     
      var json = {
        "Job_Role_Name": this.JobRoleName,  
        "Job_Role_Desc": this.JobRoleDesc,
        "Job_Role_Skills": selected_skillid,
      }
      this.axios.post('http://localhost:5000/api/jobrole', json).then((response) => {
          this.modalMessage = response.data.message + " Would you like to create another job role?"
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
<style>
h2 {
   margin: 0px !important;
}

.title {
  text-align: center;
}
</style>