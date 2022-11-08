<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal"
    v-on:btn-yes="btnYes" v-on:btn-no="btnNo" />

  <div class="container-fluid">
    <div class="row" style="margin-top:100px">
      <h2 class="title">View All Job Roles</h2>
      <p class="title">View all available job roles and their respective details</p>
    </div>

    <div class="row mb-3 justify-content-center" v-if="error.length == 0">
      <div class="table-responsive col-md-10">
        <table class="table table-striped">
          <thead class="table-success">
            <tr>
              <th scope="col">Job Role Title</th>
              <th scope="col" class="w-50">Job Role Description</th>
              <th scope="col">Job Role Status</th>
              <th scope="col" class="w25"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="val in roleData" :key="val.Title">
              <td>{{ val.Title }}</td>
              <td class="w-50">{{ val.Desc }}</td>
              <td>{{ val.Status }}</td>
              <td class="text-end">
                <button type="button" class="btn btn-outline-success" @click="ViewJobDetails(val.JobRoleID)">
                  <font-awesome-icon icon="fa-solid fa-eye"  />
                </button>
                <button type="button" class="btn btn-outline-success ms-2" @click="UpdateJobRole(val.JobRoleID)" >
                  <font-awesome-icon icon="fa-solid fa-pen" />
                </button>
                <button :disabled="val.Status != 'Active'" type="button" class="btn btn-outline-success ms-2" @click="DeleteJobRole(val.JobRoleID)">
                  <font-awesome-icon icon="fa-solid fa-trash"/>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="row" v-else>
      <div class="col col-md-4"></div>
      <div class="col col-md-4 text-center">
        <img class="img-fluid mb-3" src="../../assets/images/nodata.svg" />
        <h3>No Job Roles Registered...</h3>
      </div>
      <div class="col col-md-4"></div>
    </div>
  </div>
</template>

<script>
import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";

export default {
  name: "ViewAllJobs",
  components: {
    Loading, 
    Modal
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

<style lang="scss" scoped>
h2 {
  margin: 0px !important;
}
.title {
  text-align: center;
}
</style>