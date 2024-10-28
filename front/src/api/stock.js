import request from "@/utils/request";

export function stockList(){
    return request({
        url: '/stocks',
        method: 'GET',
    })
}

export function stockHistory(stockId){
    return request({
        url: '/stocks/' + stockId,
        method: 'GET',
    })
}

export function stockPrediction(stockId){
    return request({
        url: '/stocks/predict/' + stockId,
        method: 'GET',
    })
}