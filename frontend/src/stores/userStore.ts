import { defineStore } from 'pinia';
import type { User, SimilarUser, PageData, FilterParams, Hobby } from '../interfaces';

// Utility function to get CSRF token from cookies
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
}

type UserState = {
  userData: User | null;
  similarUsers: SimilarUser[];
  currentPage: number;
  totalPages: number;
  hobbies: Hobby[];
};

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    userData: null,
    similarUsers: [],
    currentPage: 1,
    totalPages: 1,
    hobbies: []
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

    // Add a new hobby
    async addHobby(hobbyName: string) {
      try {
        const csrfToken = getCookie('csrftoken'); // Get the CSRF token from cookies

        if (!csrfToken) {
          console.error('CSRF token not found.');
          return { success: false, error: 'CSRF token not found' };
        }

        const response = await fetch('/api/hobbies/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ name: hobbyName }),
        });

        if (!response.ok) {
          throw new Error('Failed to add hobby');
        }

        const data = await response.json();
        if (data.status === 'success') {
          await this.fetchHobbies(); // Fetch the updated list of hobbies
          return { success: true, hobby: data.hobby };
        } else {
          return { success: false, error: data.errors };
        }
      } catch (error) {
        console.error('Error adding hobby:', error);
        return { success: false, error };
      }
    },

    // Add an existing hobby to the user's profile
    async addExistingHobbyToProfile(hobbyId: number) {
      try {
        const csrfToken = getCookie('csrftoken'); // Get the CSRF token from cookies

        if (!csrfToken) {
          console.error('CSRF token not found.');
          return { success: false, error: 'CSRF token not found' };
        }

        const response = await fetch('/api/profile/add_hobby', {
          method: 'POST',
          credentials: 'include',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ hobby_id: hobbyId }),
      });

        if (!response.ok) {
          throw new Error('Failed to add hobby to profile');
        }

        const data = await response.json();
        if (data.status === 'success') {
          await this.fetchUserProfile(); // Fetch the updated user profile
          return { success: true };
        } else {
          return { success: false, error: data.errors };
        }
      } catch (error) {
        console.error('Error adding hobby to profile:', error);
        return { success: false, error };
      }
    },

    // Fetch the list of hobbies
    async fetchHobbies() {
      try {
        const response = await fetch('/api/hobbies/', {
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch hobbies');
        }
        const data = await response.json();
        this.hobbies = data.hobbies;
      } catch (error) {
        console.error('Error fetching hobbies:', error);
      }
    },

    // Fetch paginated list of users with similar hobbies
    async fetchSimilarUsers(params: FilterParams) {
      try {
        const queryParams = new URLSearchParams();
        queryParams.append('page', params.page.toString());
        if (params.minAge) queryParams.append('min_age', params.minAge.toString());
        if (params.maxAge) queryParams.append('max_age', params.maxAge.toString());

        const response = await fetch(`/api/users/similar_with_filters/?${queryParams}`, {
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }
        const data: PageData = await response.json();

        this.similarUsers = data.similar_users;
        this.currentPage = data.page;
        this.totalPages = data.total_pages;
      } catch (error) {
        console.error('Error fetching similar users:', error);
      }
    },

    async fetchPage(page: number, minAge: number | null, maxAge: number | null) {
      await this.fetchSimilarUsers({
        page,
        minAge,
        maxAge
      });
    }
  }
});
