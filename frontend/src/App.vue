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
  font-family: "ProductSansBold";
  src: url("assets/fonts/Product-Sans-Bold.ttf");
  }

  @font-face {
  font-family: "ProductSansRegular";
  src: url("assets/fonts/Product-Sans-Regular.ttf");
  }
  
  h1, h2, h3, h4, h5, h6 {
    font-family: 'ProductSansBold', Arial, sans-serif !important;
    color: #575C5F;
  }
  
  div {
    font-family: 'ProductSansRegular', Arial, Helvetica, sans-serif;
  }

  .btn-primary {
    background-color: #798E97 !important;
    border-color:  #798E97 !important;
  }

  .btn-warning {
    background-color: #C1CDD1 !important;
    border-color: #C1CDD1 !important;
  }
  
  .btn-success {
    background-color: #5D726A !important;
    border-color: #5D726A !important;
  }

  .btn-danger {
    background-color: #AF8171 !important;
    border-color: #AF8171 !important;
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
    border: 1px solid #cff5f5 !important;
    box-shadow: 0 0 10px #cff5f5 !important;
  }

  .multiselect__tags {
    border: 1px solid #cff5f5 !important;
  }

  .multiselect__tag {
    background: #5D726A !important;
  }

  .multiselect__option--highlight {
    background: #EAE6E4 !important;
    color: black !important;
  }

  .multiselect__tag-icon:after {
      color: white !important;
  }

  .table-success {
    --bs-table-color : white !important;
    --bs-table-bg :  #5D726A!important;
  }
  </style>
