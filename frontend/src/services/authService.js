import axios from 'axios';
import { toast } from 'react-toastify';

const API_URL = 'http://127.0.0.1:5000/auth';

export const register = async (userData) => {
  const val = axios.post(`${API_URL}/register`, userData).then((res)=>{
      localStorage.setItem('token', res.data.access_token);
      return true
  }).catch((res)=>{
      toast.error(res.response.data.error,{position:"top-right"})
      return false
  })
  return await val
};

export const login = async (userData) => {

  const val =  axios.post(`${API_URL}/login`, userData).then((response)=>{
      localStorage.setItem('token', response.data.access_token);
      return true
  }).catch((response)=>{
      toast.error(response.response.data.msg,{position:"top-right"})
      return false
  })

  return await val
    
};

export const logout = async () => {
  const response = await axios.post(`${API_URL}/logout`,{},{"headers":{"Authorization":`Bearer ${localStorage.getItem("token")}`}})
  localStorage.removeItem('token');
  return response.data
};

export const getCurrentUser = () => {
  return localStorage.getItem('token');
};
