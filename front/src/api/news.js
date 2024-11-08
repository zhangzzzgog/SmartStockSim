import request from "@/utils/request";

export function newsList(){
    return request({
        url: '/news',
        method: 'GET',
    })
}

export function newsInfo(newsId){
    return request({
        url: '/news/' + newsId,
        method: 'GET',
    })
}