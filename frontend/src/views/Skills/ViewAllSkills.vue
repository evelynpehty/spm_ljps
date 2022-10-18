
<template>
  <Loading v-show="loading" />

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">View All Skills</h2>
      <p class="title">View all active and retired skills</p>
    </div>
  </div>
    <br>


  <div v-if = "error.length == 0">
    <div id = "main-container" class = "container" style = "margin: auto;">
        <table id = "rolesTable" class = "table table-striped" border = "1">
            <tr>
                <th style = "text-align: center;">Skill Name</th>
                <th style = "text-align: center;">Skill Status</th>
                <!--<th style = "text-align: center;">Job Role Status</th>-->
                <th style = "text-align: center;">Actions</th>
            </tr>
            <tr v-for = "val in skillData" :key = "val.skillName">
              <td>{{val.skillName}}</td>
              <td>{{val.skillStatus}}</td>
              <!--<td>{{val.Status}}</td>-->
              <td>
                <button type="button" class="btn btn-outline-success" @click="UpdateSkill(val.skillID)" style = "margin-right: 20px;">Update</button>
                <button type="button" class="btn btn-outline-success" @click="ViewSkillDetails(val.skillID)" style = "margin-left: 20px;">View Details</button>
              </td>
            </tr>
          </table>
    </div>  
  </div>

  <div v-else>
    <h1 style = "text-align: center;">{{error}}</h1> 
  </div>

</template>

<script>
import Loading from "/src/components/Loading";

export default {
    name: "ViewAllSkillsPage",
    components: {
      Loading
    },

    data(){
      return {
        skillData: [], // list of {Title: Job_Role_Name, Desc: Job_Role_Desc}
        error: "",
        loading: null,
      }
    },
    created(){
      this.loading = true
      this.axios.get("http://127.0.0.1:5000/api/skill").then((response)=>{
        console.log(response.data.data.Skill_List)
        for (let i =0; i < response.data.data.Skill_List.length; i++){
          this.skillData.push({
            "skillID": response.data.data.Skill_List[i].Skill_ID,
            "skillName": response.data.data.Skill_List[i].Skill_Name,
            "skillStatus": response.data.data.Skill_List[i].Skill_Status
          })
        }
      }).catch(error=>{
        if (error.response.data.code == "404"){
          this.error = error.response.data.message
        }
        else {
          this.error = "Error occured in retrieving Skill Data"
        }
      }).finally(()=>{
        this.loading = false
      })
    },
    methods:{
      UpdateSkill(skillID){
        this.$router.push({name:"UpdateSkill", params: { skillID: skillID}})
      },
      ViewSkillDetails(skillID){
        this.$router.push({name: "ViewSkillDetails", params: {skillID : skillID}})
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

th {
  background-color: #5D726A;
  color: white;
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}


table {
  text-align: center;
  border: 1px solid black;
  border-spacing: 0px;
  border-width: 0px;
  padding: 0px;
  border-width: 0px;
}




</style>