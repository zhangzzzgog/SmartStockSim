package com.stock.controller;

import com.stock.result.Result;
import com.stock.service.NewsService;
import com.stock.vo.NewsVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/news")
public class NewsController {

    @Autowired
    private NewsService newsService;

    @GetMapping
    public Result<NewsVO> getNews() {
        NewsVO newsVO=newsService.getNews();
        return Result.success(newsVO);
    }
    @GetMapping("/{newsId}")
    public Result<NewsVO> getNews(@PathVariable Long newsId) {
        NewsVO newsVO=newsService.getNewsById(newsId);
        return Result.success(newsVO);
    }


}
