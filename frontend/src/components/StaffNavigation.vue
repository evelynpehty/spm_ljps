<template>
  <nav class="navbar fixed-top navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/UserMain"><img src="../assets/logo.png" height="50" width="50"></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link mx-2" href="/StaffMain">Home</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle mx-3" href="#" role="button" data-bs-toggle="dropdown">Learning Journey</a>
            <ul class="dropdown-menu mx-3">
              <li><a class="dropdown-item" href="/select-job-role">Create Learning Journey</a></li>
              <li><a class="dropdown-item" href="/manage-learning-journey">Manage Learning Journey</a></li>
            </ul>
          </li>
        </ul>
        <ul class="navbar-nav me-0 mb-2 mb-lg-0">
            <li class="nav-item">
              <button class="btn btn-success" style="cursor:pointer;" @click="signOut" >Logout</button>
            </li>
        </ul>
      </div>
    </div>
  </nav>
</template>


<script>

export default {
  name: "StaffNavigation",
  methods:{
    signOut(){
        this.$store.commit("reset");
        this.$router.push({ name: "LoginPage" });
    }
  },
}
</script>

<style scoped>
.btn {
  margin: 10px;
}
</style>