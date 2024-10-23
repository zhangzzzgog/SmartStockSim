package com.stock.exception;

public class QuantityNotEnoughException extends BaseException{
    public QuantityNotEnoughException() {
    }

    public QuantityNotEnoughException(String msg) {
        super(msg);
    }
}
