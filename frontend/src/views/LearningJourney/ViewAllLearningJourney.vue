<template>
  <Loading v-show="loading" />

  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">View Learning Journey</h2>
      <p class="title">Please select a learning journey to view more details.</p>
    </div>

    <div class="row" v-if="boolLearningJourney">
      <div class="col col-md-4"></div>
      <div class="col col-md-4 text-center">
        <img class="img-fluid mb-3" src="../../assets/images/nodata.svg" />
        <h3>No Learning Journey Registered Yet...</h3>
      </div>
      <div class="col col-md-4"></div>
    </div>

    <div class="row" v-else>
      <div class="col-lg-3 col-md-4 col-sm-6" v-for="lj, index in allLearningJourneyList" :key="lj">

        <CollapsibleCard :id="lj.Learning_Journey_ID" :targetid="lj.Learning_Journey_ID" :hidden="hidden" :cardSubtitle="'Learning Journey '+lj.Learning_Journey_ID"
        :cardTitle="this.JobRoleNameList[index]" :cardMessage="cardMessage" :btnName1="btnName1" :btnName2="btnName2" 
        :btnName3="btnName3" v-on:btn-next="btnNext" v-on:btn-update="btnNext" v-on:btn-delete="btnNext" 
        :btnHidden1="btnHidden1" :btnHidden2="btnHidden2" :btnHidden3="btnHidden3" :hiddenSubtitle="hiddenSubtitle"></CollapsibleCard>

      </div>
    </div>
  </div>
  
</template>

<script>
import Loading from "/src/components/Loading";
import CollapsibleCard from "/src/components/CollapsibleCard";

export default {
    name: "ViewAllLearningJourneysPage",

    components: {
      Loading,
      CollapsibleCard
    }, 

    data() {
      return {
        // Learning Journey Item
        LearningJourneyID : "",
        LJJobRole : "",
        JobRoleName : "",
        boolLearningJourney : false,

        // Component Item
        loading : null,
        btnName1: "View",
        btnName2: "Update",
        btnName3: "Delete",
        cardMessage: "",
        hidden: "hidden",
        btnHidden1: "",
        btnHidden2: "",
        btnHidden3: "",
        hiddenSubtitle: "",

        // Job Role Name
        LearningJourneyIDList : [],
        JobRoleIDList : [],
        JobRoleNameList : [],
        JobRoleDescList : [],
        LJ_JobRoleNameList : []
      }
    },

    created() {
      this.loading = true
      this.axios.get("http://localhost:5000/api/learningjourney/"+this.$store.state.userid).then((response)=> {
        this.allLearningJourneyList = response.data.data.LearningJourney_List
        for (var i in this.allLearningJourneyList) {
          this.axios.get("http://localhost:5000/api/jobrole/"+this.allLearningJourneyList[i].Job_Role_ID).then((response) => {
            this.JobRoleNameList.push(response.data.data.Job_Role_Name)
          }).catch(error => {
            if (error.response.data.code == "404") {
              // console.log(error.response.data)
            }
          })
        }
      }).catch(error => {
        // console.log(error.response.data)
        if (error.response.data.code == "404") {
          this.boolLearningJourney = true
        }
      }).finally(() => {
        this.loading = false
      })
  },
  
  methods : {
    btnNext(id){
      this.loading=true
      this.$router.push({name:"ViewLJDetails", params: { learningjourneyid: id } })
    },
  }
}
</script>

<style lang="scss" scoped>

</style>