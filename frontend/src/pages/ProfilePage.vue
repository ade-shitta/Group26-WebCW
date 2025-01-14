<template>
  <div v-if="userStore.userData">
    <!-- Profile Card -->
    <div class="card">
      <div class="card-body">
        <img src="#" class="avatar" alt="Profile avatar" />
        <h5 class="card-title">{{ userStore.userData?.first_name }} {{ userStore.userData?.last_name }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">@{{ userStore.userData?.username }}</h6>
        <div class="dob-email-container">
          <div class="email-container">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="email-icon"
              viewBox="0 0 16 16">
              <path
                d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z" />
            </svg>
            <div class="email-text text-muted">{{ userStore.userData?.email }}</div>
          </div>
          <div class="dob-container">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="calendar-icon"
              viewBox="0 0 16 16">
              <path
                d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z" />
            </svg>
            <div class="dob-text text-muted">{{ userStore.userData?.date_of_birth }}</div>
          </div>
        </div>
        <div class="biography">
          <p class="card-text">My name is test user and I love tennis and sketching.</p>
        </div>
        <div class="hobbies">
          <h6>My Hobbies?</h6>
        </div>
        <!-- Button trigger modal -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal"
          @click="populateEditForm">
          Edit Profile
        </button>
      </div>
    </div>

    <!-- Edit Profile Modal-->
    <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editProfileLabel">Edit Profile</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="modal-body">
              <div class="mb-3">
                <label>First Name</label>
                <input type="text" class="form-control" v-model="editForm.first_name">
              </div>
              <div class="mb-3">
                <label>Last Name</label>
                <input type="text" class="form-control" v-model="editForm.last_name">
              </div>
              <div class="mb-3">
                <label>Username</label>
                <input type="text" class="form-control" v-model="editForm.username">
              </div>
              <div class="mb-3">
                <label>Email</label>
                <input type="email" class="form-control" v-model="editForm.email">
              </div>
              <div class="mb-3">
                <label>Date of Birth</label>
                <input type="date" class="form-control" v-model="editForm.date_of_birth">
              </div>
              <div class="mb-3">
                <label>Biography</label>
                <textarea class="form-control" v-model="editForm.profile.bio" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label>Hobbies</label>
                <select multiple class="form-control" v-model="editForm.hobbies">
                  <option v-for="hobby in hobbies" :key="hobby.id" :value="hobby.id">
                    {{ hobby.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label>Add New Hobby</label>
                <div class="input-group">
                  <input type="text" class="form-control" v-model="newHobby">
                  <button class="btn btn-outline-secondary" type="button" @click="addHobby">Add</button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="saveChanges" data-bs-dismiss="modal">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import type { User, Hobby } from '../interfaces';
import { useUserStore } from '../stores/userStore';


export default defineComponent({
  mounted() {
    this.userStore.fetchUserProfile();
  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      showModal: false,
      //object for editing profile 
      editForm: {
        username: "",
        email: "",
        date_of_birth: "",
        first_name: "",
        last_name: "",
        profile: {
          bio: "",
          avatar: null
        },
        hobbies: []
      } as User, //match the User interface 
      newHobby: "",
      hobbies: [] as Hobby[] //match Hobby interface 
    };
  },
  methods: {
    populateEditForm() {
      if (this.userStore.userData) {
        this.editForm = {
          username: this.userStore.userData.username,
          email: this.userStore.userData.email,
          date_of_birth: this.userStore.userData.date_of_birth,
          first_name: this.userStore.userData.first_name,
          last_name: this.userStore.userData.last_name,
          profile: {
            bio: this.userStore.userData.profile?.bio || "",
            avatar: this.userStore.userData.profile?.avatar || null
          },
          hobbies: this.userStore.userData.hobbies || []
        };
      }
    },
    validateForm() {
      const errors = [];
      //email regex pattern
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailPattern.test(this.editForm.email)) {
        errors.push('Please enter a valid email address');
      }
      if (!this.editForm.username.trim()) {
        errors.push('Username is required');
      }
      if (!this.editForm.first_name.trim()) {
        errors.push('First name is required');
      }
      if (!this.editForm.date_of_birth) {
        errors.push('First name is required');
      }
      return errors;
    },
    //add new hobby
    addHobby() {
    },
    async saveChanges() {
      const errors = this.validateForm();
      if (errors.length) {
        return;
      }
      try {
        const result = await this.userStore.updateProfile(this.editForm);
        if (result.success) {
          console.log('Form is valid, preparing to send request. Data:', this.editForm);
          this.showModal = false;
        } else {
          // handle error
          console.error('Failed to update profile');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
});
</script>


<style scoped>
.card {
  justify-self: center;
  margin: 5rem;
  width: 30rem;
  min-height: 35rem;
}

.card-body {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 2rem;
}

.card-title {
  align-self: center;
}

.card-subtitle {
  align-self: center;
}

.btn-primary {
  display: flex;
  flex-direction: columns;
  text-decoration: none;
  margin-top: auto;
  background-color: #88D2FA;
  color: black;
  padding: 8px 16px;
  border-radius: 8px;
  align-self: center;
  border: none;
}

.card-link:hover {
  color: white;
}

.avatar {
  width: 10rem;
  height: 10rem;
  border-radius: 50%;
  object-fit: cover;
  align-self: center;
  margin-bottom: 1rem;
  border: 1px solid grey;
}

.email-container,
.dob-container {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  margin-top: 0.3rem;
}

.dob-email-container {
  display: flex;
  align-self: center;
  gap: 0.5rem;
}

.biography {
  margin-top: 0.5rem;
  align-self: center;
  padding: 0.5rem;
  font-weight: 500;
}

.hobbies h6 {
  font-weight: normal;
  justify-self: center;
}

.hobbies {
  align-self: center;
  align-content: center;
  border: 1px solid grey;
  border-radius: 1rem;
  width: 100%;
  min-height: 15rem;
  margin: 1rem;
}
</style>
