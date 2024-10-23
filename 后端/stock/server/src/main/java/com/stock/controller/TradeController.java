package com.stock.controller;

import com.stock.dto.TradeDTO;
import com.stock.result.Result;
import com.stock.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/trade")
public class TradeController {

    @Autowired
    private UserService userService;

    @PostMapping("/buy")

    public Result<String> buyStocks(@RequestBody TradeDTO tradeDTO) {
        userService.buyStocks(tradeDTO);
        return Result.success();
    }
    @PostMapping("/sell")
    public Result<String> sellStocks(@RequestBody TradeDTO tradeDTO) {
        userService.sellStocks(tradeDTO);
        return Result.success();
    }

}