import request from "@/utils/request";

export function stockList(params){
    return request({
        url: '/stocks',
        method: 'post',
        data: params,
        headers: {
            'Content-Type': 'application/json'
        }
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