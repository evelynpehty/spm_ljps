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
            <label for="JobRoleStatus" class="form-label">Job Role Status</label>
            <input type="text" class="form-control form-control-md input-border-color" id="JobRoleName" placeholder="e.g. Retired/Active" v-model="JobRoleStatus">
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

export default {
  name: "UpdateJobRole",

  components: {
    Modal,
    Loading,
    VueMultiselect,
  },

  data () {
    return {
      // Job Role Information
      jobroleid : this.$route.params.jobroleid,
      JobRoleName : "",
      JobRoleDesc : "",
      JobRoleStatus : "",
      

      // Skills
      skillList : [],
      activeSkills : [],
      selectedSkills :[],
      tempSkillList : [],
      tempActiveSkills : [],
      boolSkills : true,
      value_copy : null,

      // Comparison - Store Previous Values
      JobRoleName_Copy: "",
      JobRoleDesc_Copy: "",
      JobRoleStatus_Copy: "",
      skillList_Copy: [],
      selectedSkills_copy : [],


      // Component item
      loading: null,
      modalMessage: "Job updated Successfully. Would you like to update another job role?",
      modalActive: null,
      btnActive: true,
      value : null,

      // Errors
      errors: [],

      // Warnings
      warnings: []
    }
  },
  created() {
    this.loading = true

    this.axios.get("http://127.0.0.1:5000/api/jobrole/"+this.jobroleid).then((response)=>{
        this.JobRoleName = response.data.data.Job_Role_Name
        this.JobRoleDesc = response.data.data.Job_Role_Desc
        this.JobRoleStatus = response.data.data.Job_Role_Status
        this.skillList = response.data.data.SkillList
        

        this.JobRoleName_Copy = response.data.data.Job_Role_Name
        this.JobRoleDesc_Copy =  response.data.data.Job_Role_Desc
        this.JobRoleStatus_Copy = response.data.data.Job_Role_Status
        this.skillList_Copy =  response.data.data.SkillList

        if (this.JobRoleStatus == "Active"){
          this.value = true
          this.value_copy = true
        }
        else {
          this.value = false
          this.value_copy = false
        }

        for (var i in this.skillList){
          this.tempSkillList.push(this.axios.get("http://127.0.0.1:5000/api/skill/" + this.skillList[i].Skill_ID))
        }

        this.tempActiveSkills = this.axios.get("http://localhost:5000/api/skill/Active")
        
      }).catch(error=>{
        if (error.response.data.code == "404"){
          this.errors.push(error.response.data.message)
        }
        else {
          this.errors.push("Error occured in retrieving Job Role Data")
        }
      }).finally(()=>{
        Promise.all(this.tempSkillList).then((responses) => {
          for (var r in responses) {
            this.skillList[r]["Skill_Name"] = responses[r].data.data.Skill_Name 
          }
        }).finally(() => {
          Promise.all([this.tempActiveSkills]).then((responses) => {
            this.tempActiveSkills = responses[0].data.data.Skill_List
          }).finally(() => {
            this.selectedSkills_copy = this.skillList
            this.selectedSkills = this.skillList
            this.activeSkills = this.tempActiveSkills
            this.loading = false
          })
        })

        })
      

    
  }, 

  computed: {
      changes() {
        if (this.JobRoleName != this.JobRoleName_Copy | this.JobRoleDesc != this.JobRoleDesc_Copy | this.JobRoleStatus != this.JobRoleStatus_Copy |this.arrayEquals(this.selectedSkills, this.selectedSkills_copy) ) {
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


    UpdateJobRole() {
      var json = {
        "Job_Role_Name": this.JobRoleName,  
        "Job_Role_Desc": this.JobRoleDesc,
        "Job_Role_Status": this.JobRoleStatus,
        "Job_Role_Skills": this.selectedSkills,
      }
      console.log(json)
      this.axios.put('http://localhost:5000/api/jobrole/'+ this.jobroleid, json).then((response) => {
          this.modalMessage = response.data.message + " Would you like to update another job role?"
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
<style src="vue-multiselect/dist/vue-multiselect.css"></style>
<style lang="scss" scoped>
h2 {
   margin: 0px !important;
}

.title {
  text-align: center;
}
</style>