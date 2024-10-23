package com.stock.service;

import com.stock.vo.NewsVO;

public interface NewsService {
    NewsVO getNews();

    NewsVO getNewsById(Long newsId);
}
