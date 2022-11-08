<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>
  <div class="container-fluid">
    <div class="row" style="margin-top:100px">
      <h2 class="title">View Learning Journey</h2>
      <p class="title">Please select a learning journey to view more details.</p>
    </div>

    <div class="row" v-if="allLearningJourneyList.length == 0">
      <div class="col col-md-4"></div>
      <div class="col col-md-4 text-center">
        <img class="img-fluid mb-3" src="../../assets/images/nodata.svg" />
        <h3>No Learning Journey Registered Yet...</h3>
      </div>
      <div class="col col-md-4"></div>
    </div>

    <div class="row" v-else>
      <div class="col-lg-3 col-md-4 col-sm-6" v-for="lj in allLearningJourneyList" :key="lj">

        <CollapsibleCard :id="lj.Learning_Journey_ID" :targetid="lj.Learning_Journey_ID" :hidden="hidden" :cardSubtitle="'Learning Journey '+lj.Learning_Journey_ID"
        :cardTitle="lj.Job_Role_Name" :cardMessage="cardMessage" :btnName1="btnName1" :btnName2="btnName2" 
        :btnName3="btnName3" v-on:btn-next="btnNext" v-on:btn-update="btnUpdate" v-on:btn-delete="btnDelete" 
        :btnHidden1="btnHidden1" :btnHidden2="btnHidden2" :btnHidden3="btnHidden3" :hiddenSubtitle="hiddenSubtitle"></CollapsibleCard>

      </div>
    </div>
  </div>
  
</template>

<script>
import Loading from "/src/components/Loading";
import CollapsibleCard from "/src/components/CollapsibleCard";
import Modal from "/src/components/Modal";

export default {
    name: "ViewAllLearningJourneysPage",

    components: {
      Loading,
      CollapsibleCard,
      Modal
    }, 

    data() {
      return {
        userid : this.$store.state.userid, 
        // Learning Journey Item
        allLearningJourneyList:[],
        tempallLearningJourneyList:[],
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

        // Modal Component
        modalActive: null,
        btnActive: false,

        // Job Role Name
        LearningJourneyIDList : [],
        JobRoleIDList : [],
        JobRoleNameList : [],
        JobRoleDescList : [],
        LJ_JobRoleNameList : [],

        promises:[]
      }
    },

    beforeMount() {
      this.loading = true
      this.axios.get("http://localhost:5000/api/learningjourney/"+ this.userid).then((response) => {
        this.tempallLearningJourneyList = response.data.data.LearningJourney_List
        for(var i of this.tempallLearningJourneyList){
            (this.promises).push(this.axios.get("http://localhost:5000/api/jobrole/"+i.Job_Role_ID))
          }
      }).catch(error => {
        if (error.response.data.code == "404") {
            this.allLearningJourneyList = []
          }
        }).finally(() => {
          Promise.all(this.promises).then(responses => {
            console.log(responses)
            for(var r in responses){
              console.log(responses[r])
              this.tempallLearningJourneyList[r]["Job_Role_Name"]= responses[r].data.data.Job_Role_Name
            }
            this.allLearningJourneyList = this.tempallLearningJourneyList
            this.loading = false 
          })
        })
      },

  methods : {
    closeModal() {
      this.modalActive = !this.modalActive;
    },

    btnYes() {
      this.loading = true
      this.closeModal()
      this.axios.delete("http://127.0.0.1:5000/api/learningjourney/" + this.selectedLearningJourney).then(response => {
        if (response.data.code == 200) {
          this.modalMessage = "Learning journey " + this.selectedLearningJourney + " has been deleted successfully."}
        else {
          this.modalMessage = "Error occured in deleting learning journey. Please try again later." 
        }
      }).catch(() => {
        this.modalMessage = "Error occured in deleting learning journey. Please try again later." 
      }).finally(() => {
        this.allLearningJourneyList.splice(this.allLearningJourneyList.findIndex(e => e.Learning_Journey_ID == this.selectedLearningJourney),1)
        this.btnActive = false
        this.modalActive = true;
        this.loading = false
      })
    },

    btnNo(){
      this.closeModal()
    },

    btnNext(id){
      this.loading=true
      this.$router.push({name:"ViewLJDetails", params: { learningjourneyid: id } })
    },

    btnUpdate(id){
      this.loading=true
      this.$router.push({name:"UpdateLearningJourney", params: { learningjourneyid: id } })
    },

    btnDelete(id){
      this.selectedLearningJourney = id
      this.modalActive = true
      this.btnActive = true
      this.modalMessage = "Are you sure you want to delete Learning Journey " + id + " ?"
    }
  }
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