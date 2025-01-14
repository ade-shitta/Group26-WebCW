<template>
    <div class="container mt-4">
        <h2 class="heading">Users with Similar Hobbies</h2>

        <!-- Users List -->
        <div class="row">
            <div class="col-md-8">
                <div v-if="userStore.similarUsers.length" class="list-group">
                    <div v-for="user in userStore.similarUsers" :key="user.username"
                        class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h5>@{{ user.username }}</h5>
                            <p class="mb-1">Common hobbies: {{ user.common_hobbies }}</p>
                            <p class="mb-1">Hobbies: {{ user.hobbies.join(', ') }}</p>
                        </div>
                        <button class="btn btn-primary">Send Friend Request</button>
                    </div>
                </div>
                <p v-else>No users found with similar hobbies.</p>

                <!-- Pagination -->
                <nav v-if="userStore.totalPages > 1" class="mt-4">
                    <ul class="pagination">
                        <li class="page-item" :class="{ disabled: userStore.currentPage === 1 }">
                            <button class="page-link" @click="fetchPage(userStore.currentPage - 1)"
                                :disabled="userStore.currentPage === 1">Previous</button>
                        </li>
                        <li class="page-item" :class="{ active: userStore.currentPage === n }"
                            v-for="n in userStore.totalPages" :key="n">
                            <button class="page-link" @click="fetchPage(n)">{{ n }}</button>
                        </li>
                        <li class="page-item" :class="{ disabled: userStore.currentPage === userStore.totalPages }">
                            <button class="page-link" @click="fetchPage(userStore.currentPage + 1)"
                                :disabled="userStore.currentPage === userStore.totalPages">Next</button>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
    setup() {
        const userStore = useUserStore();
        return { userStore };
    },

    //load first page of imilar users 
    mounted() {
        this.fetchPage(1);
    },
    //fetch specific page of users with similar hobbies 
    methods: {
        fetchPage(page: number) {
            this.userStore.fetchSimilarUsers(page);
        }
    }
});
</script>
  
<style scoped>
.heading {
    text-align: center;
    margin: 1rem;
}</style>