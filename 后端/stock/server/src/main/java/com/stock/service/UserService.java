package com.stock.service;


import com.stock.dto.TradeDTO;
import com.stock.dto.UserDTO;
import com.stock.entity.User;
import com.stock.vo.BalanceVO;
import com.stock.vo.TradeHistoryVO;
import com.stock.vo.UserTradeVO;

public interface UserService {


    User login(UserDTO user);



    void register(UserDTO user);


    UserTradeVO getInfo();

    UserTradeVO getInfoBySId(Long stockId);

    void buyStocks(TradeDTO tradeDTO);

    void sellStocks(TradeDTO tradeDTO);

    TradeHistoryVO getTradeHistory();

    TradeHistoryVO getTradeHistoryBySId(Long stockId);

    BalanceVO getBalance();
}
