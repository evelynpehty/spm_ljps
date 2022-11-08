<template>
    <Loading v-show="loading" />
    <div class="container-fluid">
        <div class="row" style="margin-top:100px">
            <div class="col-12">
                <h2 class="title">View Skills Details </h2>
                <p class="title">This page shows the skill details of the respective skill.</p>
            </div>
        </div>

        <div v-if="error.length == 0">
            <div class="row mb-5 g-2 justify-content-center">
                <div class="col-sm-6 col-md-5">
                    <div class="card">
                        <div class="card-header border-bottom-0 text-center justify-content-center">
                            <h6 class="card-title mt-2">Skill Name</h6>
                            <h5 class="card-title">{{this.skillName}}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-sm-6 col-md-5">
                        <div class="card">
                        <div class="card-header border-bottom-0 text-center justify-content-center">
                            <h6 class="card-title mt-2">Skill Status</h6>
                            <h5 class="card-title">{{this.skillStatus}}</h5>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mb-3 justify-content-center" v-if="courseIDs.length == 0">
                <div class="col-sm-12 col-md-10">
                    <div class="alert alert-danger show mb-5" role="alert">
                        <h4 class="text-center m-0">No Available Courses</h4>
                    </div>
                </div>
            </div>

            <div class="row mb-3 justify-content-center" v-else>
                <div class="col-sm-12 col-md-10">
                    <h2>Courses</h2>
                </div>
                <div class="table-responsive col-sm-12 col-md-10">
                    <table class="table table-striped">
                        <thead class="table-success">
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Description</th>
                                <th>Category</th>
                                <th>Type</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="course in courseList" :key="course.Course_ID">
                            <td>{{course.Course_ID}}</td>
                            <td>{{course.Course_Name}}</td>
                            <td>{{course.Course_Desc}}</td>
                            <td>{{course.Course_Category}}</td>
                            <td>{{course.Course_Type}}</td>
                            <td>{{course.Course_Status}}</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="row mb-3 justify-content-center" v-if="jobRoleIDs.length == 0">
                <div class="col-sm-12 col-md-10">
                    <div class="alert alert-danger show mb-5" role="alert">
                        <h4 class="text-center m-0">No Available Job Roles</h4>
                    </div>
                </div>
            </div>

            <div class="row mb-3 justify-content-center" v-else>
                <div class="col-sm-12 col-md-10">
                    <h2>Job Roles</h2>
                </div>
                <div class="table-responsive col-sm-12 col-md-10">
                    <table class="table table-striped">
                        <thead class="table-success">
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Description</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="role in jobRoleList" :key="role.Job_Role_ID">
                                <td>{{role.Job_Role_ID}}</td>
                                <td>{{role.Job_Role_Name}}</td>
                                <td>{{role.Job_Role_Desc}}</td>
                                <td>{{role.Job_Role_Status}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="row m-0 mt-3" v-else>
            <div class="col col-md-4 p-0"></div>
            <div class="col col-md-4 text-center p-0 m-0">
                <img class="img-fluid mb-3" src="../../assets/images/errors.svg" />
                <h3>{{this.error}}</h3>
            </div>
            <div class="col col-md-4"></div>
        </div>

    </div>
</template>

<script>
import Loading from "/src/components/Loading";

export default {
    name: "ViewSkillDetails",
    components: {
        Loading
    },

    data() {
        return {
            skillName: '',
            skillStatus: '',
            courseIDs: [],
            courseList: [],
            jobRoleIDs: [],
            jobRoleList: [],
            error: '',
            loading: null,
        }
    },

    created() {
        this.loading = true;

        var skillID = this.$route.params.skillID 

        this.axios.get("http://127.0.0.1:5000/api/skill/" + skillID).then((response) => {
            var apiData = response.data.data

            this.skillName = apiData.Skill_Name
            this.skillStatus = apiData.Skill_Status

            if (Object.keys(apiData).length > 0) {
                for (let i=0; i<apiData.Course_List.length; i++) {
                    this.courseIDs.push(apiData.Course_List[i].Course_ID)
                }

                for (let i=0; i<apiData.Job_List.length; i++) {
                this.jobRoleIDs.push(apiData.Job_List[i].Job_Role_ID)
                }
            }

        }).catch(error => {
            if (error.response.data.code == "404"){
                this.error = error.response.data.message
            } else {
                this.error = "Error occured in retrieving Skills Data"
            }

        }).finally(() => {
            var coursePromises = []
            var rolePromises = []

            for (let i=0; i<this.courseIDs.length; i++ ) {
                coursePromises.push(this.axios.get("http://127.0.0.1:5000/api/course/id/" + this.courseIDs[i]))
            }

            for (let i=0; i<this.jobRoleIDs.length; i++ ) {
                rolePromises.push(this.axios.get("http://127.0.0.1:5000/api/jobrole/" + this.jobRoleIDs[i]))
            }

            Promise.all(coursePromises).then(response => {
                for (var r of response) {
                    this.courseList.push(r.data.data)
                }
            }).finally(()=>{
                Promise.all(rolePromises).then(response => {
                    for (var r of response) {
                        this.jobRoleList.push(r.data.data)
                    }
                }).finally(()=>{
                    this.loading = false
                })
            })
        })

    }
}

</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>

<style lang="scss" scoped>
h2 {
   margin: 0px !important;
}

.title {
  text-align: center;
}
</style>