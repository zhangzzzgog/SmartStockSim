import request from "@/utils/request";

export function userInfo(){
    return request({
        url: '/stocks/user/info',
        method: 'GET',
    })
}

export function userStockInfo(stockId){
    return request({
        url: '/stocks/user/info/' + stockId,
        method: 'GET',
    })
}

export function userTradeHistory(){
    return request({
        url: '/stocks/history',
        method: 'GET',
    })
}

export function userStockTradeHistory(stockId){
    return request({
        url: '/stocks/history/' + stockId,
        method: 'GET',
    })
}

export function user(){
    return request({
        url: '/stocks/user',
        method: 'GET',
    })
}
