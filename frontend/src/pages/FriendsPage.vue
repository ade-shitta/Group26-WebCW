<template>
    <div class="friends">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Friends</h5>
            </div>
        </div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Friend Requests</h5>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    data() {
        return {
            title: "Friends Page",
        }
    }
})
</script>
  
<style scoped>
.card {
    justify-self: center;
    margin-top: 5rem;
    width: 25rem;
    min-height: 30rem;
}

.card-body {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 1rem;
}

.card-title {
    align-self: center;
}

.friends{
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
}
</style>
  