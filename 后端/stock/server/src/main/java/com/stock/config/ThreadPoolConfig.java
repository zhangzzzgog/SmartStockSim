package com.stock.config;

import com.stock.properties.PoolProperties;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.ExecutorService;

@Configuration
public class ThreadPoolConfig {
@Autowired
PoolProperties poolProperties;
    @Bean(name = "globalPool")
    public ExecutorService globalPool() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(poolProperties.getThreadNum());
        executor.setMaxPoolSize(poolProperties.getThreadNum());
        executor.setQueueCapacity(Integer.MAX_VALUE);
        executor.setThreadNamePrefix("Async-");
        executor.initialize();
        return executor.getThreadPoolExecutor();
    }
}
