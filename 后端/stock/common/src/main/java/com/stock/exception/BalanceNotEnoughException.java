package com.stock.exception;

public class BalanceNotEnoughException extends BaseException {

    public BalanceNotEnoughException() {
    }

    public BalanceNotEnoughException(String msg) {
        super(msg);
    }

}