<template>
    <Loading v-show="loading" />

    <div class="container">

        <div v-if="error.length == 0">

            <div class="row" style="margin-top: 10%">
                <div class="col-6">
                    <div class="card">
                        <h2 class="title"> Skill Name </h2>
                        <p class="title">{{skillName}}</p>
                    </div>
                </div>

                <div class="col-6">
                    <div class="card">
                        <h2 class="title"> Skill Status </h2>
                        <p class="title">{{skillStatus}}</p>
                    </div>
                </div>
            </div>

            <div class="row">
                <div v-if="courseIDs.length == 0">
                    <h2 class="title"> No Available Courses for this skill </h2>
                </div>

                <div v-else>
                    <h2> Courses </h2>
                    <table class="table table-striped" border = "1">
                        <tr>
                            <th>Course ID</th>
                            <th>Course Name</th>
                            <th>Course Desc</th>
                            <th>Course Category</th>
                            <th>Course Type</th>
                            <th>Course Status</th>
                        </tr>

                        <tr v-for="course in courseList" :key="course.Course_ID">
                            <td>{{course.Course_ID}}</td>
                            <td>{{course.Course_Name}}</td>
                            <td>{{course.Course_Desc}}</td>
                            <td>{{course.Course_Category}}</td>
                            <td>{{course.Course_Type}}</td>
                            <td>{{course.Course_Status}}</td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="row">
                <div v-if="jobRoleIDs.length == 0">
                    <h2 class="title"> No Available Job Roles for this skill </h2>
                </div>

                <div v-else>
                    <h2> Job Roles </h2>
                    <table class="table table-striped" border = "1">
                        <tr>
                            <th>Job Role ID</th>
                            <th>Job Role Name</th>
                            <th>Job Role Desc</th>
                            <th>Job Role Status</th>
                        </tr>

                        <tr v-for="role in jobRoleList" :key="role.Job_Role_ID">
                            <td>{{role.Job_Role_ID}}</td>
                            <td>{{role.Job_Role_Name}}</td>
                            <td>{{role.Job_Role_Desc}}</td>
                            <td>{{role.Job_Role_Status}}</td>
                        </tr>
                    </table>
                </div>
            </div>

        </div>

        <div v-else>
            <h2 class="title">{{error}}</h2>
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

        // -----> ViewAllSkills.vue needs a vue method
        // ViewSkillDetails(skillID){
        //     this.$router.push({name: "ViewSkillDetails", params: {skillID : skillID}})
        // }
        //------> and a button 
        //<button type="button" class="btn btn-outline-success" @click="ViewSkillDetails(val.skillID)" style = "margin-left: 20px;">View Details</button>

        // var skillID = this.$route.params.skillID 
        var skillID = 10; //for testing
        
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
            if (error.response.data.data.code == "404"){
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
            })

            Promise.all(rolePromises).then(response => {
                for (var r of response) {
                    this.jobRoleList.push(r.data.data)
                }
            })

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

table {
text-align: center;
border: 1px solid black;
border-spacing: 0px;
border-width: 0px;
padding: 0px;
border-width: 0px;
}

.card{
padding-top: 10px;
margin-bottom: 50px;
}


</style>