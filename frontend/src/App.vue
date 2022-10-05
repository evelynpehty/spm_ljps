<template>
  <HrNavigation v-if="show==1" />
  <StaffNavigation v-if="show==2" />
  <router-view/>
</template>

<script>

import HrNavigation from "./components/HrNavigation";
import StaffNavigation from "./components/StaffNavigation";
export default {
  name: 'App',
  components: {HrNavigation, StaffNavigation},
  data() {
    //test
  },
  computed: {
    show(){
      if(this.$store.state.userrole){
        if(this.$store.state.userrole == "admin"){
          return 1
        }
        else if(this.$store.state.userrole == "staff"){
          return 2
        }
      }
      return 0
    }
  }
}
</script>

<style lang="scss">
  @font-face {
  font-family: "ShareFontRegular";
  src: url("assets/fonts/share.regular.ttf");
  }
  
  @font-face {
  font-family: "ShareFontItalic";
  src: url("assets/fonts/share.italic.ttf");
  }
  
  @font-face {
  font-family: "ShareFontBold";
  src: url("assets/fonts/share.bold.ttf");
  }
  
  h1, h2, h3, h4, h5, h6 {
    font-family: 'ShareFontBold', Arial, sans-serif !important;
    color: #575C5F;
  }
  
  div {
    font-family: 'ShareFontRegular', Arial, Helvetica, sans-serif;
  }
  
  .btn-success {
    background-color: #5D726A !important;
    border-color: #5D726A !important;
  }
  
  .btn-outline-success {
    color: #5D726A !important;
    border: 1px solid #5D726A !important
  }
  
  .btn-outline-success:hover {
    color: white !important;
    background-color: #5D726A !important;
  }
  
  .input-group-text {
    background-color: #5D726A !important;
    color: #52665F !important;
  }
  
  .input-border-color {
    border: 1px solid #cff5f5 !important;
  }
  
  .input-border-color:focus {
    outline: none !important;
    border:1px solid #cff5f5 !important;
    box-shadow: 0 0 10px #cff5f5 !important;
  }
  </style>
