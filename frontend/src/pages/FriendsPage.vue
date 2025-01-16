<template>
    <div class="container mt-4">
      <h2 class="heading">{{ title }}</h2>
  
      <!-- Friends List -->
       <div class = "flex-container">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">Friends</h5>
            <div v-if="friends.length" class="list-group">
              <div v-for="friend in friends" :key="friend.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h5>@{{ friend.friend_username }}</h5>
                  <p class="mb-1">Friends since: {{ friend.timestamp }}</p>
                </div>
              </div>
            </div>
            <p v-else class='text-center'>No friends found.</p>
          </div>
        </div>
    
        <!-- Friend Requests List -->
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Friend Requests</h5>
            <div v-if="friendRequests.length" class="list-group">
              <div v-for="request in friendRequests" :key="request.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h5>@{{ request.from_user }}</h5>
                  <p class="mb-1">Sent on: {{ request.timestamp }}</p>
                </div>
                <div>
                  <button class="btn btn-success" @click="acceptFriendRequest(request.id)">Accept</button>
                  <button class="btn btn-danger" @click="rejectFriendRequest(request.id)">Reject</button>
                </div>
              </div>
            </div>
            <p v-else class='text-center'>No friend requests found.</p>
          </div>
        </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { Friend, FriendRequest } from '../interfaces.ts';
  
  export default defineComponent({
    data() {
      return {
        title: "Friends Page",
        friends: [] as Friend[],
        friendRequests: [] as FriendRequest[],
      };
    },
    mounted() {
      this.fetchFriends(); 
      this.fetchFriendRequests(); 
    },
    methods: {
      async getCsrfToken() {
        const response = await fetch('/api/csrf-token/', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await response.json();
        return data.csrfToken;
      },
      async fetchFriends() {
        try {
          const csrfToken = await this.getCsrfToken();
          const response = await fetch('/api/friends_view/', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
          });
  
          if (!response.ok) {
            throw new Error('Failed to fetch friends');
          }
  
          const data = await response.json();
          this.friends = data.friends;
          console.log('Friends fetched successfully:', data);
        } catch (error) {
          console.error('Error fetching friends:', error);
        }
      },
      async fetchFriendRequests() {
        try {
          const csrfToken = await this.getCsrfToken();
          const response = await fetch('/api/get_friend_requests/', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
          });
  
          if (!response.ok) {
            throw new Error('Failed to fetch friend requests');
          }
  
          const data = await response.json();
          this.friendRequests = data.friend_requests;
          console.log('Friend requests fetched successfully:', data);
        } catch (error) {
          console.error('Error fetching friend requests:', error);
        }
      },
      async acceptFriendRequest(requestId: number) {
        try {
          const csrfToken = await this.getCsrfToken();
          const response = await fetch('/api/accept_request/', {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ request_id: requestId }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to accept friend request');
          }

          const data = await response.json();
          console.log('Friend request accepted successfully:', data);
          this.fetchFriendRequests(); // Refresh the friend requests list
          this.fetchFriends(); // Refresh the friends list
        } catch (error) {
          console.error('Error accepting friend request:', error);
        }
      },
      async rejectFriendRequest(requestId: number) {
        try {
          const csrfToken = await this.getCsrfToken();
          const response = await fetch('/api/reject_request/', {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ request_id: requestId }),
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to reject friend request');
          }
  
          const data = await response.json();
          console.log('Friend request rejected successfully:', data);
          this.fetchFriendRequests();
        } catch (error) {
          console.error('Error rejecting friend request:', error);
        }
      },
    }
  });
  </script>
  
  <style scoped>
  .heading {
    text-align: center;
    margin: 1rem;
  }

  .flex-container {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  }
  
  .card {
    justify-self: center;
    margin-top: 1rem;
    width: 100%;
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
  </style>