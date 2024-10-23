package com.stock.service.impl;

import com.stock.entity.News;
import com.stock.mapper.NewsMapper;
import com.stock.service.NewsService;
import com.stock.vo.NewsVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class NewsServiceImpl implements NewsService {
    @Autowired
    private NewsMapper newsMapper;
    @Override
    public NewsVO getNews() {
        NewsVO newsVO=new NewsVO();
        newsVO.setNews( newsMapper.getAllNews());
        return newsVO;
    }

    @Override
    public NewsVO getNewsById(Long newsId) {
        NewsVO newsVO=new NewsVO();
        News news=newsMapper.getNewsById(newsId);
        List<News>newsList=new ArrayList<>();
        newsList.add(news);
        newsVO.setNews( newsList);
        return newsVO;
    }
}
