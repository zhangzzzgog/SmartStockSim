<template>
    <div>
        <nav-menu></nav-menu>
        <div class="user-dashboard">
            <!-- 账户信息 -->
            <div class="account-overview">
                <h2>{{ account.username }}</h2>
                <div>
                    <p>总资产: {{ account.balance }} 元</p>
                    <p :class="priceClass(account.profit)">总收益: {{ account.profit }} 元</p>
                </div>
            </div>

            <!-- 持仓信息 -->
            <div class="stock-holdings">
                <h2>持仓信息</h2>
                <el-table :data="account.tradeInfo" class="stock-name-link" @row-click="goDetail">
                    <el-table-column prop="stockName" label="股票名称"></el-table-column>
                    <el-table-column prop="quantity" label="当前持仓量"></el-table-column>
                  <el-table-column prop="price" label="当前价格"></el-table-column>
                  <el-table-column label="总市值">
                    <template slot-scope="scope">
                      {{ (scope.row.price * scope.row.quantity).toFixed(2) }} 元
                    </template>
                  </el-table-column>
                  <el-table-column prop="cost" label="总投入"></el-table-column>
                  <el-table-column prop="earn" label="获利"></el-table-column>

                    <el-table-column label="总盈亏">
                        <template slot-scope="scope">
                            <!-- 根据盈亏动态设置样式 -->
                            <span :class="priceClass(scope.row.profit)">
                                {{ (scope.row.profit).toFixed(2) }} 元
                            </span>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <!-- 交易记录 -->
            <div class="transaction-history">
                <h2>交易记录</h2>
                <el-collapse>
                    <el-collapse-item v-for="(transaction, index) in transactions" :title="transaction.stockName"
                        :key="index">
                        <div>
                            <p>股票代码：{{ transaction.stockId }}</p>
                            <p>类型: {{ showType(transaction.tradeType) }}</p>
                            <p>价格: {{ transaction.tradePrice }}</p>
                            <p>数量: {{ transaction.tradeQuantity }}</p>
                            <p>交易时间: {{ transaction.tradeDate }}</p>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div>
        </div>
    </div>
</template>

<script>
import { userInfo, userTradeHistory } from "@/api/user";
import navMenu from "@/components/navmenu.vue";
export default {
    name: "userPage",
    components: {
        'nav-menu': navMenu,
    },
    data() {
        return {
            account: {
                username: '用户名',
                balance: 100000, // 总资产
                profit: 2000,    // 总收益
                tradeInfo: [
                    {
                        "stockId": 1,
                        "stockName": "美团",
                        "cost": 8000,
                        "quantity": 40,
                        "price": 25,
                        "value": 10000,
                        "earn": 1000,
                        "profit": 3000
                    },
                    {
                        "stockId": 2,
                        "stockName": "腾讯",
                        "cost": 9000,
                        "quantity": 20,
                        "price": 40,
                        "value": 8000,
                        "earn": 0,
                        "profit": -1000
                    }
                ],
            },
            transactions: [
                {
                    "userId": 3,
                    "stockId": 5,
                    "stockName": "阿里巴巴",
                    "tradeType": 0,
                    "tradeQuantity": 5,
                    "tradePrice": 192.0,
                    "tradeDate": "2024-10-11 22:23:52"
                },
                {
                    "userId": 3,
                    "stockId": 6,
                    "stockName": "百度",
                    "tradeType": 0,
                    "tradeQuantity": 6,
                    "tradePrice": 155.5,
                    "tradeDate": "2024-10-11 22:45:25"
                },
                {
                    "userId": 3,
                    "stockId": 7,
                    "stockName": "腾讯控股",
                    "tradeType": 0,
                    "tradeQuantity": 7,
                    "tradePrice": 360.5,
                    "tradeDate": "2024-10-11 22:46:22"
                },
                {
                    "userId": 3,
                    "stockId": 8,
                    "stockName": "京东",
                    "tradeType": 0,
                    "tradeQuantity": 8,
                    "tradePrice": 73.5,
                    "tradeDate": "2024-10-11 22:46:30"
                },
                {
                    "userId": 3,
                    "stockId": 9,
                    "stockName": "美团",
                    "tradeType": 0,
                    "tradeQuantity": 9,
                    "tradePrice": 250.5,
                    "tradeDate": "2024-10-11 22:46:36"
                },
                {
                    "userId": 3,
                    "stockId": 10,
                    "stockName": "小米",
                    "tradeType": 0,
                    "tradeQuantity": 10,
                    "tradePrice": 23.9,
                    "tradeDate": "2024-10-11 22:47:44"
                },
                {
                    "userId": 3,
                    "stockId": 5,
                    "stockName": "阿里巴巴",
                    "tradeType": 0,
                    "tradeQuantity": 3,
                    "tradePrice": 181.0,
                    "tradeDate": "2024-10-11 23:13:09"
                }
            ],
        };
    },
    created() {
        this.getUserInfo();
        //this.getUser();
        this.getHistory();
    },
    methods: {
        priceClass(profit) { //涨跌颜色
            if (profit < 0) {
                return 'price-down';
            } else {
                return 'price-up';
            }
        },
        showType(type) {//0买入1，卖出
            if (type == 0) {
                return '买入'
            }
            else if (type == 1) {
                return '卖出'
            }
        },
        getUserInfo() { //获取用戶全部信息
            userInfo().then(response => {
                this.account = response.data;
            })
        },
      goDetail(row) {
        this.$router.push({ path: `/stock/${row.stockId}` });
      },
        // getUser() { //获取用戶简要信息
        //     user().then(response => {
        //         this.account = response.data;
        //     })
        // },
        getHistory() { //交易历史
            userTradeHistory().then(response => {
                this.transactions = response.data.history;
            })
        }
    }
}
</script>

<style scoped>
.user-dashboard {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    justify-content: center;

}
.el-table th {
  border-bottom: none !important;
}
.el-table .cell {
  text-decoration: none !important;
}
.account-overview {
    background-color: #f0f0f0;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    min-width: 80%;
    max-width: 80%;
}

.stock-holdings {
    margin-top: 20px;
    min-width: 80%;
    max-width: 80%;
}

.transaction-history {
    margin-top: 20px;
    min-width: 80%;
    max-width: 80%;
}

.price-down {
    color: #01b301;
    /* 当 changePercent 是负数时，价格显示绿色 */
}

.price-up {
    color: red;
    /* 当 changePercent 是正数时，价格显示红色 */
}
.stock-name-link {
  color: #409EFF;
  cursor: pointer;
}
</style>
