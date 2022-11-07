<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal"
    v-on:btn-yes="btnYes" v-on:btn-no="btnNo" />

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">View All Roles</h2>
      <p class="title">View all available job roles and their respective details</p>
    </div>
  </div>
  <br>


  <div v-if="error.length == 0">
    <div id="main-container" class="container" style="margin: auto;">
      <table id="rolesTable" class="table table-striped" border="1">
        <tr>
          <th style="text-align: center;">Job Role Title</th>
          <th style="text-align: center;">Job Role Description</th>
          <th style="text-align: center;">Job Role Status</th>
          <th style="text-align: center;">Actions</th>
        </tr>
        <tr v-for="val in roleData" :key="val.Title">
          <td>{{ val.Title }}</td>
          <td>{{ val.Desc }}</td>
          <td>{{ val.Status }}</td>
          <td>
            <button type="button" class="btn btn-outline-success" @click="UpdateJobRole(val.JobRoleID)"
              style="margin-right: 20px;">Update</button>
            <button type="button" class="btn btn-outline-success" @click="ViewJobDetails(val.JobRoleID)"
              style="margin-left: 20px;">View Details</button>
            <button :disabled="val.Status != 'Active'" type="button" class="btn btn-outline-success"
              @click="DeleteJobRole(val.JobRoleID)" style="margin-left: 20px;">Delete</button>
          </td>
        </tr>
      </table>
    </div>
  </div>

  <div v-else>
    <h1 style="text-align: center;">{{ error }}</h1>
  </div>

</template>

<script>
import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";

export default {
  name: "ViewAllJobs",
  components: {
    Loading, Modal
  },

  data() {
    return {
      roleData: [], 
      error: "",

      selected_jobID: null,
      requestjson: null,

      loading: null,
      modelMessage: "",
      modalActive: null,
      btnActive: false
    }
  },
  created() {
    this.loading = true
    this.axios.get("http://127.0.0.1:5000/api/jobrole").then((response) => {
      for (let i = 0; i < response.data.data.Job_Role_List.length; i++) {
        this.roleData.push({
          "JobRoleID": response.data.data.Job_Role_List[i].Job_Role_ID,
          "Title": response.data.data.Job_Role_List[i].Job_Role_Name,
          "Desc": response.data.data.Job_Role_List[i].Job_Role_Desc,
          "Status": response.data.data.Job_Role_List[i].Job_Role_Status
        })
      }
    }).catch(error => {
      if (error.response.data.code == "404") {
        this.error = error.response.data.message
      }
      else {
        this.error = "Error occured in retrieving Job Role Data"
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
      this.loading = true
      this.closeModal()
      this.axios.get("http://127.0.0.1:5000/api/jobrole/" + this.selected_jobID).then((response) => {
        var apiData = response.data.data
        this.requestjson = {
          "Job_Role_Name": response.data.data.Job_Role_Name,
          "Job_Role_Desc": response.data.data.Job_Role_Desc,
          'Job_Role_Skills': [],
          "Job_Role_Status": "Retired"
        }
        for (var item of apiData.SkillList) {
          this.requestjson.Job_Role_Skills.push(item.Skill_ID)
        }
      }).catch(() => {
        this.modalMessage = "Error occured in deleting Job Role Data. Please try again later."
      }).finally(() => {
        this.axios.put("http://127.0.0.1:5000/api/jobrole/" + this.selected_jobID, this.requestjson).then((response) => {
          if (response.data.code == 201) {
            this.modalMessage = "Job Role ID: " + response.data.data.Job_Role_ID + " has been deleted successfully."

            for (var s of this.roleData) {
              if (s.JobRoleID == this.selected_jobID) {
                s.Status = "Retired"
              }
            }
          }
          else {
            this.modalMessage = "Error occured in deleting Job Role Data. Please try again later." 
          }
        }).catch(() => {
          this.modalMessage = "Error occured in deleting Job Role Data. Please try again later." 
        }).finally(() => {
          this.loading = false
          this.btnActive = false
          this.modalActive = true;
        })
      })
    },
    btnNo() {
      this.closeModal()
    },
    UpdateJobRole(jobroleid) {
      this.$router.push({ name: "UpdateJobRole", params: { jobroleid: jobroleid } })
    },
    ViewJobDetails(jobroleid) {
      this.$router.push({ name: "ViewJobDetails", params: { jobroleid: jobroleid } })
    },
    DeleteJobRole(jobroleid) {
      this.selected_jobID = jobroleid
      this.modalMessage = "Are you sure you want to delete Job Role ID: " + jobroleid + "?"
      this.modalActive = true;
      this.btnActive = true
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css">

</style>

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