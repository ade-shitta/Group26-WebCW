<template>
  <div v-if="userStore.userData">
    <!-- Profile Card -->
    <div class="card">
      <div class="card-body">
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
        <h6 class="hobbies-title">My Hobbies</h6>
        <div class="hobbies">
          <div class="table-responsive p-3">
            <table class="table">
              <tbody>
                <tr v-for="hobby in userStore.userData.hobbies" :key="typeof hobby === 'number' ? hobby : hobby.id">
                  <td class="align-middle">
                    {{ typeof hobby === 'number' ? hobby : hobby.name }}
                  </td>
                  <td class="text-end">
                    <button class="btn btn-danger btn-sm" id="deletehobby"
                      @click="deleteHobby(typeof hobby === 'number' ? hobby : hobby.id)">
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- Button trigger modal -->
        <div class="button-container">
          <button id = "edit-profile" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal"
            @click="populateEditForm">
            Edit Profile
          </button>
          <button type="button" class="btn btn-secondary ms-2" data-bs-toggle="modal" data-bs-target="#passwordModal">
            Change Password
          </button>
        </div>
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
                <input type="text" id ="editfname" class="form-control" v-model="editForm.first_name">
              </div>
              <div class="mb-3">
                <label>Last Name</label>
                <input type="text" id="editlname" class="form-control" v-model="editForm.last_name">
              </div>
              <div class="mb-3">
                <label>Username</label>
                <input type="text" id="editusername" class="form-control" v-model="editForm.username">
              </div>
              <div class="mb-3">
                <label>Email</label>
                <input type="email" id="editemail" class="form-control" v-model="editForm.email">
              </div>
              <div class="mb-3">
                <label>Date of Birth</label>
                <input type="date" id="editdob" class="form-control" v-model="editForm.date_of_birth">
              </div>
              <div class="mb-3">
                <label>Select Existing Hobby</label>
                <div class="input-group">
                  <select class="form-control" v-model="selectedHobby">
                    <option v-for="hobby in userStore.hobbies" :key="hobby.id" :value="hobby.id">
                      {{ hobby.name }}
                    </option>
                  </select>
                  <button class="btn btn-outline-secondary" type="button" @click="addExistingHobby">Add</button>
                </div>
              </div>
              <div class="mb-3">
                <label>Add New Hobby</label>
                <div class="input-group">
                  <input type="text" id="newhobbyadd" class="form-control" v-model="newHobby">
                  <button class="btn btn-outline-secondary" id="newhobbybutton" type="button" @click="addNewHobby">Add</button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button id="editsave" type="button" class="btn btn-primary" @click="saveChanges" data-bs-dismiss="modal">Save
              changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <div class="modal fade" id="passwordModal" tabindex="-1" aria-labelledby="passwordModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="passwordModalLabel">Change Password</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label>New Password</label>
              <input type="password" class="form-control" v-model="newPassword">
            </div>
            <div class="mb-3">
              <label>Confirm New Password</label>
              <input type="password" class="form-control" v-model="confirmPassword">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="changePassword" data-bs-dismiss="modal">Save
              Password</button>
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
import { getCookie } from '../stores/userStore';

export default defineComponent({
  mounted() {
    this.userStore.fetchUserProfile();
    this.userStore.fetchHobbies(); // Fetch hobbies when the component is mounted
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
        hobbies: [] as Hobby[] // Ensure hobbies field is an array of Hobby objects
      } as User,
      newHobby: "",
      selectedHobby: null,
      newPassword: '',
      confirmPassword: '',
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
        errors.push('Date of birth is required');
      }
      return errors;
    },
    async addNewHobby() {
      if (!this.newHobby.trim()) {
        alert('Hobby name cannot be empty');
        return;
      }

      const result = await this.userStore.addHobby(this.newHobby);
      if (result.success) {
        await this.userStore.fetchHobbies(); // Fetch the updated list of hobbies
        this.editForm.hobbies.push(result.hobby); // Add the new hobby to the user's list of hobbies
        if (this.userStore.userData) {
          this.userStore.userData.hobbies.push(result.hobby); // Add the new hobby to the user's list of hobbies in userData
        }
        this.newHobby = '';
      } else {
        alert('Error adding hobby: ' + JSON.stringify(result.error));
      }
    },
    async addExistingHobby() {
      if (!this.selectedHobby) {
        alert('Please select a hobby');
        return;
      }

      const result = await this.userStore.addExistingHobbyToProfile(this.selectedHobby);
      if (result.success) {
        const hobby = this.userStore.hobbies.find(hobby => hobby.id === this.selectedHobby);
        if (hobby && !this.editForm.hobbies.some(h => h.id === hobby.id)) {
          this.editForm.hobbies.push(hobby);
          if (this.userStore.userData) {
            this.userStore.userData.hobbies.push(hobby); // Add the existing hobby to the user's list of hobbies in userData
          }
        }
      } else {
        alert('Error adding hobby: ' + JSON.stringify(result.error));
      }
    },
    async deleteHobby(hobbyId: number) {
      const result = await this.userStore.deleteHobbyFromProfile(hobbyId);
      if (result.success) {
        this.editForm.hobbies = this.editForm.hobbies.filter(hobby => hobby.id !== hobbyId);
        if (this.userStore.userData) {
          this.userStore.userData.hobbies = this.userStore.userData.hobbies.filter(hobby => hobby.id !== hobbyId);
        }
      } else {
        alert('Error deleting hobby: ' + JSON.stringify(result.error));
      }
    },
    async saveChanges() {
      const errors = this.validateForm();
      if (errors.length) {
        alert(errors.join('\n'));
        return;
      }
      try {
        // Pass the array of Hobby objects directly
        const result = await this.userStore.updateProfile(this.editForm);
        if (result.success) {
          console.log('Form is valid, preparing to send request. Data:', this.editForm);
          this.showModal = false;
        } else {
          console.error('Failed to update profile');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async changePassword() {
  if (this.newPassword !== this.confirmPassword) {
    alert('Passwords do not match');
    return;
  }

  try {
    const csrfToken = getCookie('csrftoken');

    const response = await fetch('/api/profile/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      credentials: 'include',
      body: JSON.stringify({
        password: this.newPassword
      })
    });

    const data = await response.json();

    if (data.status === 'success') {
      // clear form
      this.newPassword = '';
      this.confirmPassword = '';
      alert('Password changed successfully');
    } else {
      alert('Failed to change password');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to change password');
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

.btn-primary, .btn-secondary{
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

.button-container{
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin: 1rem;
}

.card-link:hover {
  color: white;
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

.hobbies-title {
  font-weight: normal;
  align-self: center;
  margin-top: 2rem;
  margin-bottom: 0rem;
  font-weight: 500;
}

.hobbies {
  align-self: center;
  border: 1px solid grey;
  border-radius: 1rem;
  width: 100%;
  min-height: 15rem;
  margin: 1rem;
}
</style>