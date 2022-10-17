<template>
  <Loading v-show="loading" />

  <div class="container">
  <div v-if = "error.length == 0">
          <div class="row" style="margin-top:100px">
            <div class = "col-4">
              <div class = "card">
                <h2 class="title">Job Role Name</h2>
                <p class="title">{{JobRoleName}}</p>
              </div>
            </div>

            <div class = "col-4">
              <div class = "card">
                <h2 class="title">Job Role Description</h2>
                <p class="title">{{JobRoleDesc}}</p>
              </div>
            </div>

            <div class = "col-4">
              <div class = "card">
                <h2 class="title">Job Role Status</h2>
                <p class="title">{{JobRoleStatus}}</p>
              </div>
            </div>

            <br>
              <h2 class="title" style = "margin-top: 100px;">Job Role Skills</h2>
              <p v-if = "this.skillID.length == 0"  class="title">No associated skills with Job Role: {{JobRoleName}}</p>
              <br>
              <div v-if = "this.skillID.length != 0" class = "container" style = "margin: auto;">
                <table class = "table table-striped" border = "1">
                  <tr>
                    <th>Skill Name</th>
                    <th>Skill Status</th>
                  </tr>
                  <tr v-for = "val in skillList" :key = "val.Skill_ID">
                      <td>{{val.Skill_Name}}</td>
                      <td>{{val.Skill_Status}}</td>
                  </tr>
              </table>
              </div>
          </div>
      </div>
    <div v-else>
      <div class="row" style="margin-top:100px">
        <h1 style = "text-align: center;">{{this.error}}</h1> 
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

<style>
h2 {
   margin: 0px !important;
}

.title {
  text-align: center;
}

table {
text-align: center;
border: 1px solid black;
border-spacing: 0px;
border-width: 0px;
padding: 0px;
border-width: 0px;
}

.card{
padding-top: 10px;
margin-bottom: 50px;
}


</style>