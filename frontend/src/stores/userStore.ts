import { defineStore } from 'pinia';
import type { User } from '../interfaces';

type UserState = {
    userData: User | null;
};

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        userData: null,
    }),

    actions: {
        async fetchUserProfile() {
            try {
                const response = await fetch('http://localhost:8000/api/profile/', {
                    credentials: 'include'
                });
                const data = await response.json();
                this.userData = data;
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        },
        async updateProfile(updatedData: Partial<User>) {
            try {
                const response = await fetch('http://localhost:8000/api/profile/', {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(updatedData)
                });

                if (!response.ok) {
                    throw new Error('Failed to update profile');
                }

                // If successful refresh user data
                await this.fetchUserProfile();
                return { success: true };
            } catch (error) {
                console.error('Error updating profile:', error);
                return { success: false, error };
            }
        }
    }
}); 