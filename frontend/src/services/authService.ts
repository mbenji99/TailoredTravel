// src/services/authService.ts
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api/auth', // Adjust this if your backend URL differs
});

// Add JWT token to Authorization header if available
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Register User
export const registerUser = async (username: string, email: string, password: string) => {
  try {
    const response = await API.post('/register', { username, email, password });
    return {
      success: true,
      message: response.data.message,
    };
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.error || 'Signup failed. Please try again.',
    };
  }
};

// Login User
export const loginUser = async (email: string, password: string) => {
  const response = await API.post('/login', { email, password });
  return response.data; // { user_id, token, message }
};

// Reset Password
export const resetPassword = async (email: string, newPassword: string) => {
  const response = await API.post('/reset-password', { email, new_password: newPassword });
  return response.data; // { success: boolean, message: string }
};
