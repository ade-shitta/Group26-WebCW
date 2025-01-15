<template>
    <div class="container mt-4">
        <h2 class="heading">Users with Similar Hobbies</h2>

        <!-- Age Filter -->
        <div class="row mb-4">
            <div class="col-md-6 mx-auto">
                <div class="d-flex gap-3 align-items-center">
                    <input type="number" class="form-control" v-model="minAge" placeholder="Min Age" min="0">
                    <span>to</span>
                    <input type="number" class="form-control" v-model="maxAge" placeholder="Max Age" min="0">
                    <button class="btn btn-primary" @click="applyFilter">Filter</button>
                </div>
            </div>
        </div>

        <!-- Users List -->
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div v-if="userStore.similarUsers.length" class="list-group">
                    <div v-for="user in userStore.similarUsers" :key="user.username"
                        class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h5>@{{ user.username }}</h5>
                            <p class="mb-1">Common hobbies: {{ user.common_hobbies }}</p>
                            <p class="mb-1">Age: {{ user.age }}</p>
                            <p class="mb-1">Hobbies: {{ user.hobbies.join(', ') }}</p>
                        </div>
                        <button class="btn btn-primary" @click="sendFriendRequest(user.username)">Send Friend Request</button>
                    </div>
                </div>
                <p v-else class='text-center'>No users found with similar hobbies.</p>

                <!-- Pagination -->
                <nav v-if="userStore.totalPages > 1" class="mt-4">
                    <ul class="pagination justify-content-center">
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
    // initialise Pinia store
    setup() {
        const userStore = useUserStore();
        return { userStore };
    },

    data() {
        return {
            minAge: null as number | null,
            maxAge: null as number | null
        }
    },

    // load first page of similar users 
    mounted() {
        this.userStore.fetchPage(1, this.minAge, this.maxAge);
    },

    methods: {
        // apply age filter and reset to first page
        applyFilter() {
            this.userStore.fetchPage(1, this.minAge, this.maxAge);
        },

        async sendFriendRequest(username: string) {
            console.log('Sending request for username:', username);
            const result = await this.userStore.sendFriendRequest(username);
            if (result.success) {
                alert('Friend request sent!');
            } else {
                alert('Failed to send friend request!');
            }
        },

        // Update pagination method to use store
        fetchPage(page: number) {
            this.userStore.fetchPage(page, this.minAge, this.maxAge);
        }
    }
});
</script>
  
<style scoped>
.heading {
    text-align: center;
    margin: 1rem;
}
</style>