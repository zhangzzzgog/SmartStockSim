package com.stock.vo;

import com.stock.entity.TradeInfo;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserTradeVO implements Serializable {


    private static final long serialVersionUID = 1L;
    private String username;
    private Double balance;
    private Double profit;
    private List<TradeInfo> tradeInfo;


}
