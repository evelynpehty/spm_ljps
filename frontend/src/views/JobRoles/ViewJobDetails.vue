<template>
  <Loading v-show="loading" />
  <div class="container-fluid">
    <div class="row" style="margin-top:100px">
      <div class="col-12">
        <h2 class="title">View Job Role Details </h2>
        <p class="title">This page shows the job role details of the respective job role.</p>
      </div>
    </div>

    <div v-if="error.length == 0">
      <div class="row mb-5 g-2 justify-content-center">
        <div class="col-sm-6 col-md-4">
          <div class="card">
            <div class="card-header border-bottom-0 text-center justify-content-center">
                <h6 class="card-title mt-2">Job Role Name</h6>
                <h5 class="card-title">{{this.JobRoleName}}</h5>
            </div>
          </div>
        </div>
        <div class="col-sm-6 col-md-4">
          <div class="card">
            <div class="card-header border-bottom-0 text-center justify-content-center">
                <h6 class="card-title mt-2">Job Role Description</h6>
                <h5 class="card-title">{{this.JobRoleDesc}}</h5>
            </div>
          </div>
        </div>
        <div class="col-sm-12 col-md-4">
          <div class="card">
            <div class="card-header border-bottom-0 text-center justify-content-center">
                <h6 class="card-title mt-2">Job Role Status</h6>
                <h5 class="card-title">{{this.JobRoleStatus}}</h5>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-3 justify-content-center" v-if="this.skillID.length == 0">
        <div class="col-sm-12">
          <div class="alert alert-danger show mb-5" role="alert">
            <h4 class="text-center m-0">No Associated Skills with Job Role: {{JobRoleName}}</h4>
          </div>
        </div>
      </div>

      <div class="row mb-3 justify-content-center" v-else>
        <div class="col-sm-12">
            <h2>Associated Skills</h2>
        </div>
        <div class="table-responsive col-sm-12">
          <table class="table table-striped">
            <thead class="table-success">
              <tr>
                <th>Skill Name</th>
                <th>Skill Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for = "val in skillList" :key = "val.Skill_ID">
                <td>{{val.Skill_Name}}</td>
                <td>{{val.Skill_Status}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from "/src/components/Loading";

export default {
    name: "ViewJobDetails",
    components: {
      Loading
    },

    data(){
      return {
          JobRoleName: "",
          JobRoleDesc: "",
          JobRoleStatus: "",
          skillID: [], // list of skill IDs for skills associated with selected jobID 
          skillList: [],
          error: "",
          loading: null,
      }
    },
    created(){
      this.loading = true
      var jobroleid = this.$route.params.jobroleid
      this.axios.get("http://127.0.0.1:5000/api/jobrole/"+jobroleid).then((response)=>{
          this.JobRoleName = response.data.data.Job_Role_Name
          this.JobRoleDesc = response.data.data.Job_Role_Desc
          this.JobRoleStatus = response.data.data.Job_Role_Status
          if (response.data.data.SkillList.length != 0){
            for (let i = 0; i < response.data.data.SkillList.length; i++){
              this.skillID.push(response.data.data.SkillList[i].Skill_ID)
            }
          }
        
      }).catch(error=>{
        if (error.response.data.code == "404"){
          this.error = error.response.data.message
        }
        else {
          this.error = "Error occured in retrieving Job Role Data"
        }
      }).finally(()=>{
        let promises = [];

        for(var selectedSkillID of this.skillID){
          promises.push(this.axios.get("http://127.0.0.1:5000/api/skill/"+selectedSkillID))
        }

        Promise.all(promises).then(responses => {
          for(var r of responses){
            this.skillList.push(r.data.data)
          }
          this.loading = false
        })
      })
    },
    methods:{
      
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