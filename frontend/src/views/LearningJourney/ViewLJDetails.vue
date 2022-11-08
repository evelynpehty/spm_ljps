<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>

  <div class="row m-0" v-if="this.errors.length != 0" style="padding-top:250px">
    <div class="col col-md-4 p-0"></div>
    <div class="col col-md-4 text-center p-0 m-0">
      <img class="img-fluid mb-3" src="../../assets/images/errors.svg" />
      <h3>A Page Error Occurred...</h3>
    </div>
    <div class="col col-md-4"></div>
  </div>

  <div class="container-fluid" v-else>
    <div class="row" style="margin-top:100px">
      <div class="col-12">
        <h2 class="title">View Learning Journey {{this.ljID}} Details </h2>
        <p class="title">This page shows the learning journey details of the respective learning journey.</p>
      </div>
    </div>

    <div class="row mb-5 justify-content-center" v-if="this.job_role_name != ''">
      <div class="col-sm-6 col-lg-3">
        <div class="card">
          <div class="card-header border-bottom-0 text-center justify-content-center">
            <h6 class="card-title mt-2">Job Role</h6>
            <h5 class="card-title">{{this.job_role_name}}</h5>
          </div>
        </div>
      </div>
    </div> 

    <div class="row mb-3 justify-content-center" v-if="this.coursesDetails_arr.length != 0">
      <div class="table-responsive col-md-10">
        <table class="table table-striped">
          <thead class="table-success">
            <tr>
              <th scope="col">Course ID</th>
              <th scope="col">Course Name</th>
              <th scope="col">Course Status</th>
              <th scope="col">Registration Status</th>
              <th scope="col">Completion Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in this.coursesDetails_arr" :key="i">
              <th scope="row">{{i.Course_ID}}</th>
              <td>{{i.Course_Name}}</td>
              <td>{{i.Course_Status}}</td>
              <td>{{i.Registration_Status}}</td>
              <td>{{i.Completion_Status}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";

export default {
    name: "ViewLJDetails",
    components: { Loading, Modal },
    data() {
      return {
        //Data preparation
        job_role_id : "",
        temp_job_role_name : "",
        job_role_name : "",
        reg_status: "Not Registered",
        completion_status: "Not Completed",

        temp_courseList_arr: [],
        coursesDetails_arr: [],

        temp_staff_registration_arr : [],
        staff_registration_arr: [], //  all the staff's registered course details

        filter_coursesDetails_arr : [], // coursedetails + regis details of course in learning journey


        // Component item
        loading: null,
        modalMessage: null,
        modalActive: null,

        // View All Learning Journey Page
        ljID: this.$route.params.learningjourneyid,

        // Errors
        errors: [],
      }
    }, 

    beforeMount() {
      this.loading = true
      this.axios.get("http://localhost:5000/api/learningjourneybyid/" + this.ljID).then((response)=> {
        this.temp_courseList_arr = response.data.data.CourseList
        this.job_role_id = response.data.data.Job_Role_ID

        // Get Course Details from Get Course Details by ID
        for(var i of this.temp_courseList_arr){
            (this.coursesDetails_arr).push(this.axios.get("http://localhost:5000/api/course/id/"+i.Course_ID))
        }

        // Get Job Role Name from Get Job Role Details by ID
        this.temp_job_role_name = this.axios.get("http://localhost:5000/api/jobrole/"+this.job_role_id)

        // Get Registration Details from Get Registration Details by Staff ID
        this.temp_staff_registration_arr = this.axios.get("http://localhost:5000/api/registration/"+this.$store.state.userid)

      }).catch(error => {
        if (error.response.data.code == "404") {
          this.errors.push(error.response.data.message)
        }
      }).finally(() => {
        // Process Promise for Course Details
        Promise.all(this.coursesDetails_arr).then(responses => {
          for(var r in responses){
              this.temp_courseList_arr[r]["Course_Name"] = responses[r].data.data.Course_Name
              this.temp_courseList_arr[r]["Course_Status"] = responses[r].data.data.Course_Status
            }
        }).finally(() => {
          // Process Promise for Job Role ID
          Promise.all([this.temp_job_role_name]).then(responses => {
            this.temp_job_role_name = responses[0].data.data.Job_Role_Name
          }).finally(() => {

            // Process Promise for Registration
            Promise.all([this.temp_staff_registration_arr]).then(responses => {
              this.temp_staff_registration_arr = responses[0].data.data.Registration_List
              for (var x in this.temp_courseList_arr) {
                this.reg_status = "Not Registered"
                this.completion_status = "Not Completed"
                for (var i in this.temp_staff_registration_arr) {
                  if (this.temp_staff_registration_arr[i].Course_ID == this.temp_courseList_arr[x].Course_ID) {
                    this.reg_status = this.temp_staff_registration_arr[i].Reg_Status
                    if (this.temp_staff_registration_arr[i].Completion_Status != null) {
                      this.completion_status = this.temp_staff_registration_arr[i].Completion_Status
                    }
                  }
                }
                this.temp_courseList_arr[x]["Registration_Status"] = this.reg_status
                this.temp_courseList_arr[x]["Completion_Status"] = this.completion_status
              }
            }).finally(() => {
              this.coursesDetails_arr = this.temp_courseList_arr
              this.job_role_name = this.temp_job_role_name
              this.loading = false
            })
          })
        })
      })
    },
    methods: {
      DeleteLJ(id){
        this.ljID = id
        this.modalMessage = "Are you sure you want to delete Learning Journey - " + id
        this.modalActive = true  
        this.loading = false
        this.axios.delete("http://127.0.0.1:5000/api/learningjourney/" + id).then(response => {
          if (response.data.code == 200) {
            this.modalMessage = "Learning journey has been deleted successfully."}
          else {
            this.modalMessage = "Error occured in deleting learning journey. Please try again later." 
          }
        }).catch(() => {
          this.modalMessage = "Error occured in deleting learning journey. Please try again later." 
        }).finally(() => {
          this.loading = false
          this.modalActive = true
        })
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

thead, tbody {
  text-align: start !important;
}
.card-title {
  margin: 0 !important;
}

</style>