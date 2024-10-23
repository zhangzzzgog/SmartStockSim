package com.stock.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StockDetail {
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
   static public class Depths{
       private List<TradeEx>asks;
       private List<TradeEx>bids;


    }
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    static public class TradeEx {
        private Double price;
        private Integer volume;
    }
    private StockSummary stockSummary;
    private List<RecentPrice> lines;
    private Depths depths;

}
