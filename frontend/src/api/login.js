import request from "@/utils/request";

//登录
export function login(username, password) {
    const data = {
        username,
        password
    }
    return request({
        url: '/login',
        method: 'POST',
        data: data
    })
}

//注册
export function register(username, password) {
    const data = {
        username,
        password
    }
    return request({
        url: '/register',
        method: 'POST',
        data: data
    })
}