
<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal"
    v-on:btn-yes="btnYes" v-on:btn-no="btnNo" />
  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h2 class="title">View All Skills</h2>
      <p class="title">View all active and retired skills</p>
    </div>
  </div>
  <br>


  <div v-if="error.length == 0">
    <div id="main-container" class="container" style="margin: auto;">
      <table id="rolesTable" class="table table-striped" border="1">
        <tr>
          <th style="text-align: center;">Skill Name</th>
          <th style="text-align: center;">Skill Status</th>
          <!--<th style = "text-align: center;">Job Role Status</th>-->
          <th style="text-align: center;">Actions</th>
        </tr>
        <tr v-for="val in skillData" :key="val.skillName">
          <td>{{ val.skillName }}</td>
          <td>{{ val.skillStatus }}</td>
          <td>

            <button type="button" class="btn btn-outline-success" @click="ViewSkillDetails(val.skillID)">View</button>
            <button type="button" class="btn btn-outline-success" @click="UpdateSkill(val.skillID)"
              style="margin-left: 20px;">Update</button>
            <button :disabled="val.skillStatus != 'Active'" type="button" class="btn btn-outline-success"
              @click="DeleteSkill(val.skillID)" style="margin-left: 20px;">Delete</button>
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
  name: "ViewAllSkills",
  components: {
    Loading, Modal
  },

  data() {
    return {
      skillData: [],
      error: "",

      selected_skillID: null,
      requestjson: null,

      loading: null,
      modalMessage: "",
      modalActive: null,
      btnActive: false
    }
  },
  created() {
    this.loading = true
    this.axios.get("http://127.0.0.1:5000/api/skill").then((response) => {
      for (let i = 0; i < response.data.data.Skill_List.length; i++) {
        this.skillData.push({
          "skillID": response.data.data.Skill_List[i].Skill_ID,
          "skillName": response.data.data.Skill_List[i].Skill_Name,
          "skillStatus": response.data.data.Skill_List[i].Skill_Status
        })
      }
    }).catch(error => {
      if (error.response.data.code == "404") {
        this.error = error.response.data.message
      }
      else {
        this.error = "Error occured in retrieving Skill Data"
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
      this.axios.get("http://127.0.0.1:5000/api/skill/" + this.selected_skillID).then((response) => {
        var apiData = response.data.data
        this.requestjson = {
          "Skill_Name": response.data.data.Skill_Name,
          "Course_Skills": [],
          "Skill_Status": "Retired"
        }
        for (var item of apiData.Course_List) {
          (this.requestjson.Course_Skills).push(item.Course_ID)
        }
      }).catch(() => {
        this.modalMessage = "An error has occurred while deleting the skill. Please try again."
      }).finally(() => {
        this.axios.put("http://127.0.0.1:5000/api/skill/" + this.selected_skillID, this.requestjson).then((response) => {

          if (response.data.code == 201) {
            this.modalMessage = "Skill ID - " + response.data.data.Skill_ID + " is now retired"

            for (var s of this.skillData) {
              if (s.skillID == this.selected_skillID) {
                s.skillStatus = "Retired"
              }
            }

          }
          else {
            this.modalMessage = "An error has occurred while deleting the skill. Please try again."
          }

        }).catch(() => {
          this.modalMessage = "An error has occurred while deleting the skill. Please try again."
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
    UpdateSkill(skillID) {
      this.$router.push({ name: "UpdateSkill", params: { skillID: skillID } })
    },
    ViewSkillDetails(skillID) {
      this.$router.push({ name: "ViewSkillDetails", params: { skillID: skillID } })
    },
    DeleteSkill(skillID) {
      this.modalMessage = "Are you sure you want to retire SkillID - " + skillID
      this.btnActive = true
      this.selected_skillID = skillID
      this.modalActive = true
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