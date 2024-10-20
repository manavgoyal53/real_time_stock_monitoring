import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/auth';

export const register = async (userData) => {
  const response = await axios.post(`${API_URL}/register`, userData);
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
};

export const login = async (userData) => {

  const response = await axios.post(`${API_URL}/login`, userData);
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const getCurrentUser = () => {
  return localStorage.getItem('token');
};
