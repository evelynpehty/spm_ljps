
<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal"
    v-on:btn-yes="btnYes" v-on:btn-no="btnNo" />
  <div class="container-fluid">
    <div class="row" style="margin-top:100px">
      <h2 class="title">View All Skills</h2>
      <p class="title">View all skills and their respective details</p>
    </div>

    <div class="row mb-3 justify-content-center" v-if="error.length == 0">
      <div class="table-responsive col-md-10">
        <table class="table table-striped">
          <thead class="table-success">
            <tr>
              <th scope="col">Skill Name</th>
              <th scope="col">Skill Status</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="val in skillData" :key="val.skillName">
              <td>{{ val.skillName }}</td>
              <td>{{ val.skillStatus }}</td>
              <td class="text-end">
                <button type="button" class="btn btn-outline-success" @click="ViewSkillDetails(val.skillID)">
                  <font-awesome-icon icon="fa-solid fa-eye"  />
                </button>
                <button type="button" class="btn btn-outline-success ms-2" @click="UpdateSkill(val.skillID)" >
                  <font-awesome-icon icon="fa-solid fa-pen" />
                </button>
                <button :disabled="val.skillStatus != 'Active'" type="button" class="btn btn-outline-success ms-2" @click="DeleteSkill(val.skillID)">
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
        <h3>No Skills Registered...</h3>
      </div>
      <div class="col col-md-4"></div>
    </div>
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

<style src="vue-multiselect/dist/vue-multiselect.css"></style>

<style lang="scss" scoped>
h2 {
  margin: 0px !important;
}

.title {
  text-align: center;
}
</style>