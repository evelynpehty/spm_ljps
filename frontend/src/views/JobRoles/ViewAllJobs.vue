<template>
  <Loading v-show="loading" />

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">View All Roles</h2>
      <p class="title">View all available job role and their respective job descriptions</p>
    </div>
  </div>
    <br>


  <div v-if = "error.length == 0">
    <div id = "main-container" class = "container" style = "margin: auto;">
        <table id = "rolesTable" class = "table table-striped" border = "1">
            <tr>
                <th style = "text-align: center;">Job Role Title</th>
                <th style = "text-align: center;">Job Role Description</th>
                <th></th>
            </tr>
            <tr v-for = "val in roleData" :key = "val.Title">
              <td>{{val.Title}}</td>
              <td>{{val.Desc}}</td>
              <td><button type="button" class="btn btn-outline-success" @click="UpdateJobRole(val.JobRoleID)">Update</button></td>
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
    name: "ViewAllJobs",
    components: {
      Loading
    },

    data(){
      return {
        roleData: [], // list of {Title: Job_Role_Name, Desc: Job_Role_Desc}
        error: "",
        loading: null,
      }
    },
    created(){
      this.loading = true
      this.axios.get("http://127.0.0.1:5000/api/jobrole/Active").then((response)=>{
        //console.log(response.data.data.Job_Role_List)
        for (let i =0; i < response.data.data.Job_Role_List.length; i++){
          this.roleData.push({
            "JobRoleID": response.data.data.Job_Role_List[i].Job_Role_ID,
            "Title": response.data.data.Job_Role_List[i].Job_Role_Name,
            "Desc": response.data.data.Job_Role_List[i].Job_Role_Desc,
          })
        }
      }).catch(error=>{
        if (error.response.data.code == "404"){
          this.error = error.response.data.message
        }
        else {
          this.error = "Error occured in retrieving Job Role Data"
        }
      }).finally(()=>{
        this.loading = false
      })
    },
    methods:{
      UpdateJobRole(jobroleid){
        this.$router.push({name:"UpdateJobRole", params: { jobroleid: jobroleid}})
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

}
</style>