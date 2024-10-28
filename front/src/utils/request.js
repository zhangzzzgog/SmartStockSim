import axios from 'axios';

// 创建 axios 实例
const service = axios.create({
    baseURL: 'http://localhost:8080/api', // 后端的基础请求地址
    timeout: 5000 // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
    (config) => {

        const token = localStorage.getItem('token');

        if (token) {
            config.headers['Authorization'] = token;
        }

        return config;
    },
    (error) => {
        // 处理请求错误
        return Promise.reject(error);
    }
);

// 响应拦截器
service.interceptors.response.use(
    (response) => {
        // 可以在这里统一处理响应数据
        return response.data;
    },
    (error) => {
        // 可以在这里统一处理响应错误
        return Promise.reject(error);
    }
);

export default service;