import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api/auth', 
});

// Signup API (with name, email, and password)
export const registerUser = async (username: string, email: string, password: string) => {
  const response = await API.post('/register', { username, email, password });
  return response.data;
};


// Login API 
export const loginUser = async (email: string, password: string) => {
  const response = await API.post('/login', { email, password });
  return response.data;
};
