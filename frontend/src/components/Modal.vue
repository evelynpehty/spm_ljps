<template>
  <div class="modal">
    <div class="modal-content">
      <div class="d-flex justify-content-end">
         <i class="fa fa-times-circle" style="color: #5ac2c2" @click="closeModal"></i>
      </div>
      <div class="d-flex justify-content-center align-items-center text-center mt-3 mx-5">
         <p v-html="modalMessage"></p>
      </div>
      <div v-if="this.btnActive" class="d-flex justify-content-center align-items-center text-center mb-5 mx-5">
        <button type="button" class="btn btn-success me-3" @click="btnYes">Yes</button>
        <button type="button" class="btn btn-danger" @click="btnNo">No</button>
      </div>
     
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalComponent",
  props: ["modalMessage", "btnActive", "path"],
  methods: {
    closeModal() {
      this.$emit("close-modal");
    },
    btnYes() {
      this.$emit("btn-yes");
    },
    btnNo() {
      this.$emit("btn-no");
    },
  },
};
</script>

<style lang="scss" scoped>
.modal {
  top: 0;
  z-index: 101;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;

  .modal-content {
    border-radius: 8px;
    width: 500px;
    height: auto;
    padding: 10px;
    background-color: white;
  }
}
</style>
