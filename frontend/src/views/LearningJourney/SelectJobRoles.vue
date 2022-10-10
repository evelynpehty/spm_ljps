<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">Start a New Learning Journey Now</h2>
      <p class="title">Please select a job role below to view the necessary skills and courses needed.</p>
    </div>

    <div class="row" v-if="boolJobRoles">
      <div class="col col-md-4"></div>
      <div class="col col-md-4 text-center">
        <img class="img-fluid mb-3" src="../../assets/images/nodata.svg" />
        <h3>No Available Job Roles...</h3>
      </div>
      <div class="col col-md-4"></div>
    </div>

    <div class="row" v-else>
      <div class="col-lg-3 col-md-4 col-sm-6" v-for="job in activeJobRoles" :key="job">
        <CollapsibleCard :id="job.Job_Role_ID" :targetid="job.Job_Role_ID" :cardTitle="job.Job_Role_Name" :cardMessage="job.Job_Role_Desc" :btnName="btnName" v-on:btn-next="btnNext"></CollapsibleCard>
      </div>
    </div>

  </div>
</template>

<script>
import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";
import CollapsibleCard from "/src/components/CollapsibleCard";

export default {
  name: "SelectJobRolesPage",

  components: {
  Loading,
  Modal,
  CollapsibleCard
  },

  data() {
    return {
      // Job Role Information
      JobRoleName : "",
      JobRoleDesc : "",
      boolJobRoles : false,

      // Component item
      loading: null,
      cardMessage: "",
      targetid: "",
      btnName: "Set as Goal",
      id: "",
      modalActive: null,
      btnActive: true,

      // Staff Learning Journey
      registered_job_roles: []
    }
  }, 

  created() {
    this.loading = true
    this.axios.get("http://localhost:5000/api/jobrole/Active").then((response)=> {
      this.activeJobRoles = response.data.data.Job_Role_List
      // console.log(this.activeJobRoles)
    }).catch(error => {
      // console.log(error.response.data)
      if (error.response.data.code == "404") {
        this.boolJobRoles = true
        // console.log(this.activeJobRoles)
      }
    }).finally(() => {
      this.loading = false
    })
  },

  methods: {
    btnNext(id){
      // console.log(id)
      this.axios.get("http://localhost:5000/api/learningjourney/"+this.$store.state.userid).then((response) => {
        this.staffLearningJourney = response.data.data.LearningJourney_List
        for (var lj in this.staffLearningJourney) {
          this.registered_job_roles.push(this.staffLearningJourney[lj].Job_Role_ID)
        }
        // console.log(this.registered_job_roles.includes(id))
        if (this.registered_job_roles.includes(id)) {
          this.modalMessage = "Learning Journey with Selected Job Role already exist!"
          this.modalActive = true
          this.btnActive = false
        } else {
          this.$router.push({name:"CreateLearningJourney", params: { jobroleid: id } })
        }

      }).catch(error => {
        // console.log(error.response.data)
        if (error.response.data.code == "404") {
          this.$router.push({name:"CreateLearningJourney", params: { jobroleid: id } })
        }
      }).finally(() => {
        this.loading = false
      })
    },

    closeModal() {
      this.modalActive = null;
    },
  }
}
</script>

<style lang="scss" scoped>
  h2 {
    margin: 0px !important;
  }

  h3 {
    color: #AF8171 !important;
  }

  .title {
    text-align: center;
  }
</style>