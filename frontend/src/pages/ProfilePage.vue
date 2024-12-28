<template>
  <!-- Profile Card -->
  <div class="card">
    <div class="card-body">
      <img src="..." class="avatar" alt="..."></img>
      <h5 class="card-title">Name</h5>
      <h6 class="card-subtitle mb-2 text-muted">@username</h6>
      <div class="dob-email-container">
        <div class="email-container">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="email-icon"
            viewBox="0 0 16 16">
            <path
              d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z" />
          </svg>
          <div class="email-text text-muted">username@gmail.com</div>
        </div>
        <div class="dob-container">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="calendar-icon"
            viewBox="0 0 16 16">
            <path
              d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z" />
          </svg>
          <div class="dob-text text-muted">day/month/year</div>
        </div>
      </div>
      <div class="biography">
        <p class="card-text">My name is test user and I love tennis and sketching.</p>
      </div>
      <div class="hobbies">
        <h6>My Hobbies</h6>
      </div>
        <!-- Button trigger modal -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal"> Edit Profile </button>
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
              <label>Name</label>
              <input type="text" class="form-control" v-model="editForm.name">
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
              <input type="date" class="form-control" v-model="editForm.dob">
            </div>
            <div class="mb-3">
              <label>Biography</label>
              <textarea class="form-control" v-model="editForm.bio" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label>Hobbies</label>
              <select multiple class="form-control" v-model="editForm.selectedHobbies">
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
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
//not actually saved to backend yet 
export default defineComponent({
  data() {
    return {
      showModal: false,
      //object for editing profile 
      editForm: {
        name: "",
        username: "",
        email: "",
        date_of_birth: "",
        bio: "",
        hobbies: []
      },
      newHobby: "",
    };
  },
  methods: {
    //add new hobby
    addHobby() {
    },
    saveChanges() {
      this.showModal = false;
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

.btn-primary{
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
}</style>
