<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">Update Job Role</h2>
      <p class="title">Please edit the required fields accordingly to update job role</p>
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
            <label for="JobRoleName" class="form-label">Job Role Name</label>
            <input type="text" class="form-control form-control-md input-border-color" id="JobRoleName" placeholder="e.g. Software Engineer" v-model="JobRoleName">
          </div>

          <div class="mb-3">
            <label for="JobRoleDesc" class="form-label">Job Role Description</label>
            <textarea class="form-control form-control-md input-border-color" placeholder="e.g. Will be tasked to code the frontend of application." id="floatingTextarea" style="height: 100px;" v-model="JobRoleDesc"></textarea>
          </div>

          <div class="mb-3">
            <label for="JobRoleSkills" class="form-label">Existing Job Role Skills</label>
            <p v-if = "this.existingSkillID.length == 0"  class="title">No associated skills with Job Role: {{JobRoleName}}</p>
              <br>
              <div v-if = "this.existingSkillID.length != 0" class = "container" style = "margin: auto;">
                <table class = "table table-striped" border = "1">
                  <tr>
                    <th>Skill Name</th>
                    <th>Skill Status</th>
                    <th>Action</th>
                  </tr>
                  <tr v-for = "val in existingSkillList" :key = "val.Skill_ID">
                      <td>{{val.Skill_Name}}</td>
                      <td>{{val.Skill_Status}}</td>
                      <td><button type="button" class="btn btn-outline-success" @click="RemoveSkill(val.Skill_ID)" style = "margin-right: 20px;">Remove</button></td>
                  </tr>
              </table>
              </div>
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
            <button type="submit" class="btn btn-success p-2">Update</button>
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
  name: "UpdateJobRole",

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
      existingSkillID : [],
      existingSkillList : [],

      // Skills
      activeSkills : [],
      boolSkills : true,
      selectedSkills :[],


      // Component item
      loading: null,
      modalMessage: "Job updated Successfully. Would you like to update another job role?",
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

    var jobroleid = this.$route.params.jobroleid
    this.axios.get("http://127.0.0.1:5000/api/jobrole/"+jobroleid).then((response)=>{
        this.JobRoleName = response.data.data.Job_Role_Name
        this.JobRoleDesc = response.data.data.Job_Role_Desc
        if (response.data.data.SkillList.length != 0){
          for (let i = 0; i < response.data.data.SkillList.length; i++){
            this.existingSkillID.push(response.data.data.SkillList[i].Skill_ID)
          }
        }
        console.log()
      }).catch(error=>{
        if (error.response.data.code == "404"){
          this.errors.push(error.response.data.message)
        }
        else {
          this.errors.push("Error occured in retrieving Job Role Data")
        }
      }).finally(()=>{
        let promises = [];

        for(var selectedSkillID of this.existingSkillID){
          promises.push(this.axios.get("http://127.0.0.1:5000/api/skill/"+selectedSkillID))
        }

        Promise.all(promises).then(responses => {
          for(var r of responses){
            this.existingSkillList.push(r.data.data)
          }
          this.loading = false
        })
      })

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

      if (this.JobRoleDesc.length > 255) {
        this.warnings.push("Job Description is too long! It should not exceed 255 characters. Please try again!")
      }
      console.log(this.warnings)

      if (this.errors.length == 0 && this.warnings.length == 0) {
        this.UpdateJobRole()
      }
    },

    resetField() {
      this.JobRoleName = "";
      this.JobRoleDesc = "";
      this.SelectedSkills = ""
    },

    RemoveSkill(skillid){

      for (let i=0; i<this.existingSkillID.length; i++){
        if(this.existingSkillID[i] == skillid){
          this.existingSkillID.splice(i,1)
        }
      }

      for (let j=0; j<this.existingSkillList.length; j++){
        if(this.existingSkillList[j].Skill_ID == skillid){
          this.existingSkillList.splice(j,1)
        }
      }

    },

    UpdateJobRole(jobid) {
      var selected_skillid = []

      for (let i=0; i<this.existingSkillID.length; i++){
        selected_skillid.push(this.existingSkillID[i])
        }

      for(var j of this.selectedSkills){
        if (!selected_skillid.includes(j)){
          selected_skillid.push(j.Skill_ID)
        }
      }
      this.loading = true;
     
      var json = {
        "Job_Role_Name": this.JobRoleName,  
        "Job_Role_Desc": this.JobRoleDesc,
        "Job_Role_Skills": selected_skillid,
      }
      console.log(json)
      this.axios.post('http://localhost:5000/api/jobrole'+jobid, json).then((response) => {
          this.modalMessage = response.data.message + " Would you like to update another job role?"
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