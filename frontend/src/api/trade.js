import request from "@/utils/request";

export function buyStock(stockId, quantity){
    const data = {
        stockId: stockId, //请注意这里两个数据都是int类型，stockId可能需要parseInt
        quantity: quantity
    }
    return request({
        url: '/trade/buy',
        method: 'POST',
        data: data
    })
}

export function sellStock(stockId, quantity){
    const data = {
        stockId: stockId, //请注意这里两个数据都是int类型，stockId可能需要parseInt
        quantity: quantity
    }
    return request({
        url: '/trade/sell',
        method: 'POST',
        data: data
    })
}