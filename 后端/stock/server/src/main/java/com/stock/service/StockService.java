package com.stock.service;


import com.stock.entity.StockDetail;
import com.stock.entity.StockPredict;
import com.stock.entity.StockSummary;

import java.util.List;

public interface StockService {


    public List<StockSummary> getAllStockSummaries();


    StockDetail getStockDetail(Long stockId);

    StockPredict getStockPredict(Long stockId);
}
