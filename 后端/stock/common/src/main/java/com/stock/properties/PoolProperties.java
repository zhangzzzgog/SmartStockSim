package com.stock.properties;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "stock.pool")
@Data
public class PoolProperties {
    private Integer threadNum;
}
