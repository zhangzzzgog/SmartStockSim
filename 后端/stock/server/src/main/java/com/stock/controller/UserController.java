package com.stock.controller;
import com.stock.constant.JwtClaimsConstant;
import com.stock.dto.UserDTO;
import com.stock.entity.User;
import com.stock.properties.JwtProperties;
import com.stock.result.Result;
import com.stock.service.UserService;
import com.stock.utils.JwtUtil;
import com.stock.vo.BalanceVO;
import com.stock.vo.TradeHistoryVO;
import com.stock.vo.UserTradeVO;
import com.stock.vo.UserVO;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 员工管理
 */
@RestController
@RequestMapping("/api")
@Slf4j
@Api(tags = "登录相关接口")
public class UserController {

    @Autowired
    private UserService userService;
    @Autowired
    private JwtProperties jwtProperties;


    @PostMapping("/login")
    @ApiOperation(value = "用户登录")
    public Result<UserVO> login(@RequestBody UserDTO userDTO) {
        log.info("用户登录：{}", userDTO.getUsername());

        User user = userService.login(userDTO);

        //登录成功后，生成jwt令牌
        Map<String, Object> claims = new HashMap<>();
        claims.put(JwtClaimsConstant.USER_ID, user.getId());
        String token = JwtUtil.createJWT(
                jwtProperties.getAdminSecretKey(),
                jwtProperties.getAdminTtl(),
                claims);

        UserVO userVO = UserVO.builder()
                .id(user.getId())
                .token(token)
                .build();

        return Result.success(userVO);
    }



    @PostMapping("/register")
    @ApiOperation(value = "新增用户")
    public Result<String> register(@RequestBody UserDTO userDTO){
        log.info("注册用户：{}", userDTO);
        //调用service层新增员工
        userService.register(userDTO);
        return Result.success();
    }

    @GetMapping("/stocks/user")
    public Result<BalanceVO> getBalance(){
        BalanceVO balanceVO=userService.getBalance();
        return Result.success(balanceVO);
    }
    @GetMapping("/stocks/user/info")
    public Result<UserTradeVO> getUserInfo(){
        UserTradeVO userTradeVO=userService.getInfo();
        return Result.success(userTradeVO);
    }

    @GetMapping("/stocks/user/info/{stockId}")
    public Result<UserTradeVO> getInfoBySId(@PathVariable Long stockId){
        UserTradeVO userTradeVO=userService.getInfoBySId(stockId);
        return Result.success(userTradeVO);
    }
    @GetMapping("/stocks/history")
    public Result<TradeHistoryVO> getTradeHistory(){
        TradeHistoryVO tradeHistoryVO=userService.getTradeHistory();
        return Result.success(tradeHistoryVO);
    }

    @GetMapping("/stocks/history/{stockId}")
    public Result<TradeHistoryVO> getTradeHistoryBySId(@PathVariable Long stockId){
        TradeHistoryVO tradeHistoryVO=userService.getTradeHistoryBySId(stockId);
        return Result.success(tradeHistoryVO);
    }




}

