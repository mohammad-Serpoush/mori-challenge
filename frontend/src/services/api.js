// api.js
import axios from 'axios';

const API_URL = 'http://5.182.86.26:8000'; 

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// CRUD operations

export const getAllProductsBySemantic = async (query) => {
  try {
    const response = await api.get('/products/semantic?' + query);
    return response.data;
  } catch (error) {
    throw error;
  }
};


export const getAllProductsByFullText = async (query) => {
  try {
    const response = await api.get('/products/full-text?' + query);
    return response.data;
  } catch (error) {
    throw error;
  }
};






export default api;
