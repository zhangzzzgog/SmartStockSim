package com.stock.vo;

import com.stock.entity.TradeHistroy;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TradeHistoryVO {
    List<TradeHistroy> history;
}
