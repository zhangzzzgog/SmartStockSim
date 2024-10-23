package com.stock.controller;

import com.stock.entity.StockDetail;
import com.stock.entity.StockPredict;
import com.stock.entity.StockSummary;
import com.stock.result.Result;
import com.stock.service.StockService;
import com.stock.vo.StockSummaryVO;
import org.apache.poi.ss.formula.CollaboratingWorkbooksEnvironment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadPoolExecutor;

@RestController
@RequestMapping("/api/stocks")
public class StockController {
    static  Logger logger= LoggerFactory.getLogger(StockController.class);
    @Autowired
    private StockService stockService;


    @GetMapping
    public Result<StockSummaryVO> getAllStocks() {
        logger.info("Start get all stock info");
        Long time1=System.currentTimeMillis();
        List<StockSummary> stockSummaries = stockService.getAllStockSummaries();
        Long time2=System.currentTimeMillis()-time1;
        logger.info("Finish get stock info,spend {}",time2);
        StockSummaryVO stocks=new StockSummaryVO();
        stocks.setStocks(stockSummaries);
        return Result.success(stocks);
    }
    @GetMapping("/{stockId}")
    public Result<StockDetail> getStockDetail(@PathVariable Long stockId) {
        StockDetail stockDetail = stockService.getStockDetail(stockId);
        return Result.success(stockDetail);
    }

    @GetMapping("/predict/{stockId}")
    public Result<StockPredict> getStockPredict(@PathVariable Long stockId) {
        StockPredict stockPredict = stockService.getStockPredict(stockId);
        return Result.success(stockPredict);
    }
}
