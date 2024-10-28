<template>
  <div>
    <nav-menu style="margin-bottom: 10px"></nav-menu>
    <div class="stock-container">
      <el-card class="stock-card" v-for="(stock, index) in stocks" :key="index">
        <div class="stock-title">
          <span class="title"> {{ stock.stockName }} ({{ stock.stockCode }}) </span>
          <span class="current-price" :class="priceClass(stock)">{{ stock.price }}</span>
        </div>
        <div class="stock-info">
          <p class="info">昨收 {{ stock.closingPrice }}</p>
          <p class="info">今高 {{ stock.maxPrice }}</p>
          <p class="info">今低 {{ stock.minPrice }}</p>
          <p class="info">今日成交量 {{ stock.volume }}</p>
          <span class="change-percent" :class="priceClass(stock)">{{ stock.changePercent }}%</span>
        </div>
      </el-card>
    </div>
    <el-backtop></el-backtop>
  </div>
</template>

<script>
import navMenu from "@/components/navmenu.vue";
import { stockList } from "@/api/stock"
export default {
  name: "homePage",
  components: {
    'nav-menu': navMenu
  },
  data(){
    return{
      stocks: [
        {
          "stockId": 1,
          "stockName": "百度",
          "stockCode": "A41",
          "price": 13874.5,
          "closingPrice": 13974.2,
          "maxPrice": 14012.2,
          "minPrice": 13231.1,
          "changePercent": -0.007,
          "volume": 6712
        },
        {
          "stockId": 2,
          "stockName": "美团",
          "stockCode": "B42",
          "price": 13874.5,
          "closingPrice": 13974.2,
          "maxPrice": 14012.2,
          "minPrice": 13231.1,
          "changePercent": -0.007,
          "volume": 6712
        }
      ]
    }
  },
  created() {
    this.getStockList();
  },
  methods: {
    priceClass(stock) { //涨跌颜色
      if (stock.changePercent < 0) {
        return 'price-down';
      } else {
        return 'price-up';
      }
    },
    getStockList(){ //获取主页股票列表，后续挂载到created
      stockList().then(response => {
        this.stocks = response.data.stocks;
      })
    }
  }
}
</script>


<style scoped>
.stock-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.stock-card {
  position: relative;
  margin: 10px;
  padding-left: 15px;
  padding-right: 10px;
  width: 60%;
  &::before,
  &::after{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
    box-sizing: border-box;
    border: 1px solid #2e95ff;
    transition: clip-path .5s ease-in-out;
  }
  &::before{
    clip-path: inset(0 75% 60% 0);
  }
  &::after{
    clip-path: inset(60% 0 0 75%);
  }
  &:hover{
    &::before,
    &::after{
      clip-path: inset(0 0 0 0);
    }
  }
}

.el-card__body, .el-main{
  padding: 10px;
}

.current-price{
  float: right;
  font-size: 22px;
  margin-right: 10px;
  font-weight: bold;
}

.change-percent{
  float: right;
  font-size: 14px;
  margin-right: 10px;
}

.title{
  font-size: 24px;
  font-weight: bold;
}

.price-down {
  color: #01b301; /* 当 changePercent 是负数时，价格显示绿色 */
}

.price-up {
  color: red; /* 当 changePercent 是正数时，价格显示红色 */
}

.stock-info{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-top: 0;
}

p{
  margin-bottom: 0;
}

.info{
  padding-top: 5px;
}

</style>