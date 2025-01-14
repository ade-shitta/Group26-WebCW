import { defineStore } from 'pinia';
import type { User } from '../interfaces';

// Utility function to get CSRF token from cookies
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
}

type UserState = {
  userData: User | null;
};

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    userData: null,
  }),

  actions: {
    // Fetch the user profile
    async fetchUserProfile() {
      try {
        const response = await fetch('http://localhost:8000/api/profile/', {
          credentials: 'include', // Send cookies along with the request
        });
        if (!response.ok) {
          if (response.status === 403 || response.status === 401) {
            window.location.href = 'http://localhost:8000/login/';
            return;
          }
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.userData = data;
      } catch (error) {
        console.error('Error fetching profile:', error);
        window.location.href = 'http://localhost:8000/login/';
      }
    },

    // Update the user profile
    async updateProfile(updatedData: Partial<User>) {
      try {
        const csrfToken = getCookie('csrftoken'); // Get the CSRF token from cookies

        if (!csrfToken) {
          console.error('CSRF token not found.');
          return { success: false, error: 'CSRF token not found' };
        }

        const response = await fetch('http://localhost:8000/api/profile/', {
          method: 'PUT',
          credentials: 'include', // Ensure cookies are included
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include CSRF token in headers
          },
          body: JSON.stringify(updatedData), // Send updated user data
        });

        if (!response.ok) {
          throw new Error('Failed to update profile');
        }

        // If successful, refresh user data
        await this.fetchUserProfile();
        return { success: true };
      } catch (error) {
        console.error('Error updating profile:', error);
        return { success: false, error };
      }
    },
  },
});
