<template>
  <Loading v-show="loading" />
  <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
  <div class="container-fluid">
    <div class="row" style="margin-top:80px">
      <h3></h3>
    </div>
  </div>
</template>

<script>
import Loading from "/src/components/Loading";
import Modal from "/src/components/Modal";

export default {
    name: "ViewLJDetails",
    components: { Loading, Modal },
    data() {
    return {
        //data preparation
        staff_registration_arr: [], //  all the staff's registered course details
        coursesDetails_arr: [], // all the course from database
        filter_coursesDetails_arr : [], // coursedetails + regis details of course in learning journey

        // Component item
        loading: null,
        modalMessage: null,
        modalActive: null,
        }
    }, 
    created(){

    }
}
</script>

<style>

</style>