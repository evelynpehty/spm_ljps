<template>
  <Loading v-show="loading" />

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">View All Roles</h2>
      <p class="title">View all job role titles and their respective job descriptions</p>
    </div>
  </div>
    <br>


  <div v-if = "error.length == 0">
    <div id = "main-container" class = "container" style = "margin: auto;">
        <h3 style = "text-align: center;">Available Organizational Roles</h3> 
        <table id = "rolesTable" class = "table table-striped" border = "1">
            <tr>
                <th style = "text-align: center;">Role Title</th>
                <th style = "text-align: center;">Role Description</th>
            </tr>
            <tr v-for = "val in roleData" :key = "val.Title">
              <td>{{val.Title}}</td>
              <td>{{val.Desc}}</td>
            </tr>
          </table>
    </div>  
  </div>

  <div v-if = "error.length != 0">
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
        console.log(response.data.Job_Role_List)
        for (let role in response.data.Job_Role_List){
          console.log(role)
          this.roleData.append(role.Job_Role_Name,role.Job_Role_Desc)
        }
        console.log(this.roleData)
      }).catch(error=>{
        console.log(error.code)
        if (error.code == "404"){
          this.error = error.message
        }
        else {
          this.error = "Error occured in retrieving Job Role Data"
        }
      }).finally(()=>{
        this.loading = false
      })
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
  background-color: #04AA6D;
  color: white;
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>