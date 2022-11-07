<template>
    <div class="card shadow-sm mb-3">
        <div class="card-header collapsible cursor-pointer rotate" data-bs-toggle="collapse" :data-bs-target="'#target'+targetid">
            <h6 class="card-title mt-2" :style="hiddenSubtitle" v-html="cardSubtitle"></h6>
            <h3 class="card-title" v-html="cardTitle"></h3>
            <div class="card-toolbar rotate-180"></div>
        </div>
        
        <div :id="'target'+targetid" class="collapse" :hidden="hidden">
            <div class="card-body">
                <p v-html="cardMessage"></p>
            </div>
        </div>

        <div class="card-footer">
            <button type="button" class="btn btn-sm btn-primary me-2" :id="id" @click="btnNext(id)" v-html="btnName1" :style="btnHidden1"></button>
            <button type="button" class="btn btn-sm btn-warning me-2" :id="id" @click="btnUpdate(id)" v-html="btnName2" :style="btnHidden2"></button>
            <button type="button" class="btn btn-sm btn-danger me-2" :id="id" @click="btnDelete(id)" v-html="btnName3" :style="btnHidden3"></button>
        </div>
    </div>
</template>

<script>
    export default {
      name: "CollapsibleCardComponent",
      props: ["cardSubtitle", "cardTitle", "cardMessage", "targetid", "btnName1", "btnName2", "btnName3", "id", "hidden", "btnHidden1", "btnHidden2", "btnHidden3", "hiddenSubtitle"],
      methods: {
        btnNext(id) {
            this.$emit("btn-next", id);
        },

        btnUpdate(id) {
            this.$emit("btn-update", id);
        },

        btnDelete(id) {
            this.$emit("btn-delete", id);
        }
      }
    };
</script>

<style lang="scss" scoped>
.card {
    padding: 0px !important;
}
.card-header {
    background-color: #AF8171 !important;
    border: none;
}

.card-title {
    color: white !important;
}

.btn-primary {
    background-color: #6D7275 !important;
    border-color:  #6D7275 !important;
}
</style>