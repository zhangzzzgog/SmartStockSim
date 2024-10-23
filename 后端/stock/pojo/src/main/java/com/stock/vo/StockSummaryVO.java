package com.stock.vo;

import com.stock.entity.StockSummary;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StockSummaryVO {
    private List<StockSummary>stocks;
}
