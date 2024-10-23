package com.stock.entity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RecentPrice{
    private String time;
    private Double price;
    private Double open_price;
    private Double close_price;
    private Double max_price;
    private Double min_price;
    private Integer volume;

}

