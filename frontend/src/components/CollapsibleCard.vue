<template>
    <div class="card shadow-sm mb-5">
        <div class="card-header collapsible cursor-pointer rotate" data-bs-toggle="collapse" :data-bs-target="'#target'+targetid">
            <h3 class="card-title" v-html="cardTitle"></h3>
            <div class="card-toolbar rotate-180"></div>
        </div>
        
        <div :id="'target'+targetid" class="collapse">
            <div class="card-body">
                <p v-html="cardMessage"></p>
            </div>
        </div>

        <div class="card-footer">
            <button type="button" class="btn btn-sm btn-primary" :id="id" @click="btnNext(id)" v-html="btnName"></button>
        </div>
    </div>
</template>

<script>
    export default {
      name: "CollapsibleCardComponent",
      props: ["cardTitle", "cardMessage", "targetid", "btnName", "id"],
      methods: {
        btnNext(id) {
            this.$emit("btn-next", id);
        }
      }
    };
</script>

<style lang="scss" scoped>
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