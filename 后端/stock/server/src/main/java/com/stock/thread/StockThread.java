package com.stock.thread;

import com.stock.entity.StockSummary;
import com.stock.mapper.StockMapper;
import com.stock.vo.StockSummaryVO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.concurrent.CountDownLatch;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class StockThread extends Thread{
    private CountDownLatch countDownLatch;
    private String code;
    private List<StockSummary> stockSummaries;
    private StockMapper stockMapper;
    @Override
    public void run(){
        try {
            if(stockMapper.findIdByCode(code)==null)
                stockMapper.insertStockId(code);
            StockSummary summary = stockMapper.findStockSummaryByCode(code);
            if (summary != null) {
                stockSummaries.add(summary);
            }
        }
      finally {
            countDownLatch.countDown();
        }

    }

}
