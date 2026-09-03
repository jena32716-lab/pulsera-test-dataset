import axios from 'axios';

const API = axios.create({ baseURL: process.env.REACT_APP_API_URL || '' })

export default {
  predictFile: (file) => {
    const fd = new FormData();
    fd.append('file', file);
    return API.post('/predict', fd)
  }
}
