package com.stock.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TradeDTO implements Serializable {

    private static final long serialVersionUID = 1L;


    private Long stockId;


    private Integer quantity;



}
