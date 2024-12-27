<template>
        <!-- Header -->
        <header class ="main-header">
            <div class="nav-links">
                <router-link class="" :to="{ name: 'Profile Page' }">
                    Profile Page
                </router-link>
                <router-link class="" :to="{ name: 'Other Page' }">
                    Other Page
                </router-link>
            </div>
        </header>
        <RouterView class="flex-shrink-0" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>

<style scoped>

.main-header{
    background-color:#88D2FA;
    margin: 0 rem;
    padding: 1.5rem;
}

.nav-links{
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
                 
}

</style>
