export interface User {
  username: string;
  email: string;
  date_of_birth: string | null;
  first_name: string;
  last_name: string;
  hobbies: Hobby[];
}

export interface Profile {
    bio: string; 
    avatar: File | string | null;
}

export interface Hobby {
    id: number; 
    name: string; 
    created_at: string;
    created_by: string | null; 
}

export interface SimilarUser {
    username: string;
    common_hobbies: number;
    hobbies: string[];
    age: number;
  }
  
  export interface PageData {
    page: number;
    total_pages: number;
    total_users: number;
    users_per_page: number;
    similar_users: SimilarUser[];
  }

  export interface FilterParams {
    page: number;
    minAge?: number | null;
    maxAge?: number | null;
  }