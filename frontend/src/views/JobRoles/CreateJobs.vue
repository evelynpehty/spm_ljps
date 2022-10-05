<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">Create Job Role</h2>
      <p class="title">Please fill in the required fields to successfully create a job role.</p>
    </div>
    <br>

    <div v-if="errors.length != 0" class="row">
      <div class="alert alert-danger mb-5" role="alert">
        <h4>Please check your inputs</h4>
        <ul>
          <li class="m-0" v-for="e in errors" :key="e"> {{e}}</li>
        </ul>
      </div>
    </div>

    <div class="card border-0 shadow p-3 mb-5 bg-white rounded">
      <div class="card-body">
        <form @submit.prevent v-on:submit="checkForm">
          <div class="form-floating mb-3">
            <input type="text" class="form-control form-control-md input-border-color" id="JobRoleName" placeholder="Enter Job Role Name..." v-model="JobRoleName" required>
            <label for="JobRoleName">Job Role Name</label>
          </div>

          <div class="form-floating mb-3">
            <textarea class="form-control form-control-md input-border-color" placeholder="Enter Job Role Description..." id="floatingTextarea" style="height: 100px;" v-model="JobRoleDesc" required></textarea>
            <label for="JobRoleDesc">Job Role Description</label>
          </div>

          <div v-if="boolSkills" class="form-floating mb-3">
            <select class="form-select input-border-color" id="JobRoleSkills" aria-label="Floating label select example">
              <option>Select a Skill...</option>
              <option v-for="(item, index) in activeSkills" :key="index" :id="item.Skill_ID" :value="item.Skill_ID">{{item.Skill_Name}}</option>
            </select>
            <label for="floatingSelect">Skills affiliated with Job Role</label>
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

export default {
  name: "CreateJobRolesPage",

  components: {
    Modal,
    Loading
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
      modalMessage: "Job Created Successfully. Create Another?",
      modalActive: null,
      btnActive: true,
    
      // Errors
      errors: []
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
      this.resetField()
    },

    btnNo(){
      //this.$router.push({name:"OrgMain"})
    },

    checkForm(){
      this.errors = [];

      if (this.JobRoleName.trim().length == 0) {
        this.errors.push("Job Role Name is empty! Please enter Job Role Name.")
      }

      if (this.JobRoleDesc.trim().length == 0) {
        this.errors.push("Job Role Description is empty! Please enter Job Role Description.")
      }

      if (this.selectedSkills.length == 0) {
        this.errors.push("No Skills selected! Please select at least 1 skill.")
      }

      if (this.errors.length == 0) {
        this.CreateJobRole()
      } else {
        console.log(this.errors)
      }
    },

    resetField() {
      this.JobRoleName = "";
      this.JobRoleDesc = "";
      this.SelectedSkills = ""
    },

    CreateJobRole() {
      this.loading = true;
      var json = {
        "Job_Role_Name": this.JobRoleName,  
        "Job_Role_Desc": this.JobRoleDesc,
        "Job_Role_Skills": this.selectedSkills,
      }
      console.log(this.selectedSkills)
      this.axios.post('http://localhost:5000/api/jobrole', json).then((response) => {
          this.modalMessage = response.data.message + " Create Another?"
          this.btnActive = true
        }).catch(error => {
            this.modalMessage = error.response.data.data.message 
            this.btnActive = false
        }).finally(() => {
            this.loading = false
            this.modalActive = true; 
          })
    }

  }

}
</script>

<style>
h2 {
   margin: 0px !important;
}

.title {
  text-align: center;
}
</style>