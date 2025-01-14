export interface User {
    username: string;
    email: string; 
    date_of_birth: string | null; 
    first_name: string; 
    last_name: string; 
    profile: Profile; 
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
}

export interface PageData {
    similar_users: SimilarUser[];
    page: number;
    total_pages: number;
}