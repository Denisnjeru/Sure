import axios from 'axios';
import Cookies from 'js-cookie';
import router from '../router'
import store from '../store'
import NProgress from 'vue-nprogress'
const nprogress = new NProgress()


export const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 90000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    // 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
  },
});

instance.interceptors.request.use((config) => {
  nprogress.start()
  const accessToken = Cookies.get('token');
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
}, function (error) {
  nprogress.done()
  return Promise.reject(error)
});

// before a response is returned stop nprogress
instance.interceptors.response.use(response => {
  nprogress.done()
  return response
}, function (error) {
  nprogress.done()
  if (error.response.status === 401 && error.response.config.url !== '/authentication/login') {
    window.toast.fire({
      icon: 'error',
      title: 'Session timed out. Please login to continue.'
    })
    store.dispatch('Auth/logout')
    store.dispatch('User/logout')    
    router.push('/login')
  }
  return Promise.reject(error)
})

const api = {
  request(method, url, data, successMsg = null, errorMsg = null) {
    instance.request({
      url,
      data,
      method: method.toLowerCase(),
    }).then(successMsg).catch(errorMsg);
  },

  get(url, success = null, errorMsg = null) {
    return this.request('get', url, {}, success, errorMsg);
  },

  post(url, data, success = null, errorMsg = null) {
    return this.request('post', url, data, success, errorMsg);
  },

  put(url, data, success = null, errorMsg = null) {
    return this.request('put', url, data, success, errorMsg);
  },

  patch(url, data, success = null, errorMsg = null) {
    return this.request('patch', url, data, success, errorMsg);
  },

  delete(url, data = {}, success = null, errorMsg = null) {
    return this.request('delete', url, data, success, errorMsg);
  },
};

export default api;