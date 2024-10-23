package com.stock.mapper;

import com.stock.entity.News;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface NewsMapper {
    @Select("select id,title,description,published_at,news.detail from stock.news ")
    List<News> getAllNews();

    @Select("select id,title,description,published_at,detail from stock.news where id=#{newsId} ")
    News getNewsById(Long newsId);
}
