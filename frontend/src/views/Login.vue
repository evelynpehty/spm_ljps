<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
  <section class="vh-100" style="background-color: #CCD8DB;">
    <div class="container h-100">
      <div class="row d-flex flex-wrap justify-content-center align-items-center h-100">
        <div class="col col-xl-10">
          <div class="card p-3" style="border-radius: 1rem;">
  
            <div class="row g-0">
  
              <div class="col-md-6 col-lg-5 d-none d-md-block my-auto">
                <img
                  src="../assets/images/register.png"
                  alt="login"
                  class="img-fluid" style="border-radius: 1rem 0 0 1rem;"
                />
              </div>
  
              <div class="col-md-6 col-lg-7 d-flex align-items-center">
                <div class="card-body p-4 p-lg-3 text-black">
  
                  <form @submit.prevent v-on:submit="login">
  
                    <h3 class="fw-normal mt-5 mb-3 pb-3" style="letter-spacing: 1px;">Learning Journey Planning System</h3>
  
                    <div class="form-outline mb-4">
                      <label class="form-label" for="email">Email</label>
                      <input type="email" placeholder="Enter Email" class="form-control form-control-lg input-border-color" id="email" v-model="email" required />
                    </div>
  
                    <div class="form-outline mb-4">
                      <label for="password" class="form-label">Password</label>
                      <input type="password" placeholder="Enter Password..." class="form-control form-control-lg input-border-color" id="password" v-model="password" required/>
                    </div>
  
                    <div class="d-grid mb-2">
                      <button type="submit" class="btn btn-success p-2">Login</button>
                    </div>
                  </form>
  
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
  
<script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";

export default {
    name: "LoginPage",
    data() {
        return {
        email: null,
        password: "",
        loading: null,
        modalMessage: null,
        modalActive: null,
        };
    },
    components: {
       Loading, Modal
    },
    methods: {
      closeModal() {
      this.modalActive = !this.modalActive;
    },
      login(){
         this.loading = true;
         var email = this.email
         var roleid;
         var rolename;
         var name ;
         var staffid;
             
         this.axios.get('http://localhost:5000/api/staff/'+email).then((response) => {
             roleid = response.data.data.Role
             name = response.data.data.Staff_FName + " " + response.data.data.Staff_LName
             staffid = response.data.data.Staff_ID
         }).catch(() => { 
            this.modalActive = true
            this.loading = false;
            this.modalMessage = "Incorrect username/password"
          }).finally(()=>{
            this.axios.get('http://localhost:5000/api/role/'+roleid).then((response) => {
              rolename = response.data.data.Role_Name 
            }).catch(() => { 
                this.modalActive = true
                this.loading = false;
                this.modalMessage = "role does not exist"
            }).finally(()=>{
              var setjson;
              if(rolename == "Admin" & this.password =="admin"){
              setjson= {"userid":staffid, "userrole":"admin", "username":name}
              this.$store.commit("setuserInfo", setjson)
              this.$router.push({ name: "HrMain" }); 
              }
              else if(rolename != "Admin" & this.password =="staff"){
                setjson= {"userid":staffid, "userrole":"staff", "username":name}
                this.$store.commit("setuserInfo", setjson)
                this.$router.push({ name: "StaffMain" });
              }
              this.modalActive = true
              this.loading = false;
              this.modalMessage = "Incorrect username/password"
            })
          })
      }
    }
}
</script>
