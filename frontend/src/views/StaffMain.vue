<template>
      
    <div class="container-fluid">
      <div class="row" style="margin-top:100px">
        <h3>Hello {{name}}</h3>
      </div>
    </div>
            
</template>
        
<script>
    export default {
    name: "StaffMain",
    data() {
        return {
        name: this.$store.state.username,
        
        };
    },
    }
</script>
    