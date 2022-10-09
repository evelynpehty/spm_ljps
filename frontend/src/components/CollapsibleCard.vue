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
    </div>
</template>

<script>
    export default {
      name: "CollapsibleCardComponent",
      props: ["cardTitle", "cardMessage", "targetid"],
    };
    </script>