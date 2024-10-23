package com.stock.service.impl;

import com.stock.entity.RecentPrice;
import com.stock.entity.StockDetail;
import com.stock.entity.StockPredict;
import com.stock.entity.StockSummary;
import com.stock.mapper.StockMapper;
import com.stock.service.StockService;
import com.stock.thread.StockThread;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;

@Service
public class StockServiceImpl implements StockService {

    @Autowired
    private StockMapper stockMapper;
    @Autowired
    ExecutorService globalPool;

    public List<StockSummary> getAllStockSummaries() {
        // Step 1: 获取所有不同的股票代码
        List<String> stockCodes = stockMapper.findAllStockCodes();
        // Step 2: 根据每个股票代码获取简要信息
        List<StockSummary> stockSummaries = Collections.synchronizedList(new ArrayList<>());
        CountDownLatch countDownLatch=new CountDownLatch(stockCodes.size());
        for (String stockCode : stockCodes) {
            StockThread stockThread=new StockThread(countDownLatch,stockCode,stockSummaries,stockMapper);
            globalPool.execute(stockThread);
        }
        try {
            countDownLatch.await();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        stockSummaries.sort(Comparator.comparing(StockSummary::getStockCode));
        return stockSummaries;
    }

    @Override
    public StockDetail getStockDetail(Long stockId) {
        String code=stockMapper.findCodeById(stockId);
        StockDetail stockDetail=new StockDetail();
        stockDetail.setStockSummary(stockMapper.findStockSummaryByCode(code));
        List<RecentPrice>recentPrices=stockMapper.findRecentPricesByCode(code);
        recentPrices.sort(Comparator.comparing(RecentPrice::getTime));
        stockDetail.setLines(recentPrices);
        List<StockDetail.TradeEx> asks=new ArrayList<>();
        List<StockDetail.TradeEx> bids=new ArrayList<>();
        for(RecentPrice recentPrice:recentPrices){
            Double price=recentPrice.getPrice();
            Integer volume=recentPrice.getVolume();
            Integer asksVolume=volume/3+new Random().nextInt(volume*2/3);
            Integer bidsVolume=volume-asksVolume;
            asks.add(new StockDetail.TradeEx(price,asksVolume));
            bids.add(new StockDetail.TradeEx(price,bidsVolume));
        }
        stockDetail.setDepths(new StockDetail.Depths(asks,bids));
        return stockDetail;
    }

    @Override
    public StockPredict getStockPredict(Long stockId) {
        return null;
    }
}
