<template>
  <Loading v-show="loading" />

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">Start a New Learning Journey Now</h2>
      <p class="title">Please select a job role below to view the necessary skills and courses needed.</p>
    </div>

    <div class="row">
      <div class="col-lg-3 col-md-4 col-sm-6" v-for="job in activeJobRoles" :key="job">
        <CollapsibleCard :targetid="job.Job_Role_ID" :cardTitle="job.Job_Role_Name" :cardMessage="job.Job_Role_Desc"></CollapsibleCard>
      </div>
    </div>

  </div>
</template>

<script>
import Loading from "/src/components/Loading";
import CollapsibleCard from "/src/components/CollapsibleCard";
// import StepProgress from 'vue-step-progress';

export default {
  name: "CreateLearningJourneyPage",

  components: {
  Loading,
  CollapsibleCard
  // 'step-progress': StepProgress
  },

  data() {
    return {
      // mySteps: ['Step 1', 'Step 2', 'Step 3'],
      // currentStep: 1

      // Job Role Information
      JobRoleName : "",
      JobRoleDesc : "",

      // Component item
      loading: null,
      cardMessage: "",
      targetid: ""
    }
  }, 

  created() {
    this.loading = true
    this.axios.get("http://localhost:5000/api/jobrole/Active").then((response)=> {
      this.activeJobRoles = response.data.data.Job_Role_List
      console.log(this.activeJobRoles)
    }).catch(error => {
      // console.log(error.response.data)
      if (error.response.data.code == "404") {
        this.boolJobRoles = false
      }
    }).finally(() => {
      this.loading = false
    })
  }, 
}
</script>

<style lang="scss" scoped>
  h2 {
    margin: 0px !important;
  }

  .title {
    text-align: center;
  }
</style>