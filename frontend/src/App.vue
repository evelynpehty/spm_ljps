<template>
  <router-view/>
</template>

<script>


export default {
  name: 'App',
  components: {
    
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
    color: #5ac2c2;
  }
  
  div {
    font-family: 'ShareFontRegular', Arial, Helvetica, sans-serif;
  }
  
  .btn-success {
    background-color: #5ac2c2 !important;
    border-color: #5ac2c2 !important;
  }
  
  .btn-outline-success {
    color: #5ac2c2 !important;
    border: 1px solid #5ac2c2 !important
  }
  
  .btn-outline-success:hover {
    color: white !important;
    background-color: #5ac2c2 !important;
  }
  
  .input-group-text {
    background-color: #cff5f5 !important;
    color: #5ac2c2 !important;
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
