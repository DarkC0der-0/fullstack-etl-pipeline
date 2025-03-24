import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const fetchPipelineStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/pipeline-status`);
    return response.data;
  } catch (error) {
    console.error('Error fetching pipeline status:', error);
    throw error;
  }
};

export const fetchPipelineLogs = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/pipeline-logs`);
    return response.data;
  } catch (error) {
    console.error('Error fetching pipeline logs:', error);
    throw error;
  }
};