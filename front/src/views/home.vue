
<template>
  <div v-loading.fullscreen="isLoading">
    <nav-menu style="margin-bottom: 15px"></nav-menu>
    <div class="search-container">
      <el-input class="search-input" v-model="searchCode" placeholder="输入股票代码"></el-input>
      <el-input class="search-input-name" v-model="searchName" placeholder="输入股票名称"></el-input>
      <el-button type="primary" @click="getStockList" plain icon="el-icon-search">搜索</el-button>
    </div>
    <div class="stock-container">
      <el-card class="stock-card" v-for="(stock, index) in stocks" :key="index" @click.native="goDetail(stock.stockId)">
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
    <div class="pagination-container">
      <el-pagination
          v-if="total > pageSize"
          background
          layout="prev, pager, next"
          :current-page.sync="currentPage"
          :page-size="pageSize"
          :total="total"
          @current-change="handlePageChange">
      </el-pagination>
    </div>
    <el-backtop></el-backtop>
  </div>
</template>
<script>
import navMenu from "@/components/navmenu.vue";
import { stockList } from "@/api/stock";

export default {
  name: "homePage",
  components: {
    'nav-menu': navMenu
  },
  data() {
    return {
      stocks: [],
      isLoading: true,
      searchCode: localStorage.getItem('stockCode')&&localStorage.getItem('stockCode')!=='null'? localStorage.getItem('stockCode') :'',
      searchName: localStorage.getItem('stockName')&&localStorage.getItem('stockName')!=='null'? localStorage.getItem('stockName') :'',
      currentPage: localStorage.getItem('currentPage')&&localStorage.getItem('currentPage')!=='null'?Number(localStorage.getItem('currentPage')):1 ,
      pageSize: 10,
      total: 0
    };
  },
  created() {
    this.getStockList();
  },
  methods: {
    priceClass(stock) {
      if (stock.changePercent < 0) {
        return 'price-down';
      } else {
        return 'price-up';
      }
    },
    getStockList() {
      this.isLoading = true;
      const params = {
        page: this.currentPage,
        pageSize: this.pageSize,
        stockCode: this.searchCode,
        stockName: this.searchName
      };
      stockList(params).then(response => {
        this.stocks = response.data.stocks;
        this.total = response.data.total;
        this.isLoading = false;
      });
      this.saveSearchParams();
      },
    saveSearchParams() {
      localStorage.setItem('stockName', this.searchName);
      localStorage.setItem('stockCode', this.searchCode);
      localStorage.setItem('currentPage', this.currentPage);
    },
    goDetail(stockId) {
      this.$router.push({ path: `/stock/${stockId}` });
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.getStockList();
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
  margin: 7px;
  padding-left: 15px;
  padding-right: 10px;
  width: 60%;
  &::before,
  &::after {
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
  &::before {
    clip-path: inset(0 75% 60% 0);
  }
  &::after {
    clip-path: inset(60% 0 0 75%);
  }
  &:hover {
    &::before,
    &::after {
      clip-path: inset(0 0 0 0);
    }
  }
}

/deep/ .stock-card .el-card__body{
  padding: 15px;
}

.current-price {
  float: right;
  font-size: 22px;
  margin-right: 10px;
  font-weight: bold;
}

.change-percent {
  float: right;
  font-size: 14px;
  margin-right: 10px;
}

.title {
  font-size: 24px;
  font-weight: bold;
}

.price-down {
  color: #01b301;
}

.price-up {
  color: red;
}

.stock-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-top: 0;
}

p {
  margin-top: 3px;
  margin-bottom: 0;
}

.info {
  padding-top: 5px;
}

.search-input {
  width: 20%;
}

/deep/ .search-input .el-input__inner {
  border-radius: 10px;
}

.search-input-name{
  width: 65%;
}

/deep/ .search-input-name .el-input__inner {
  border-radius: 10px;
}

.el-button{
  border-radius: 10px;
}

.search-container {
  display: flex;
  justify-content: space-between;
  width: 60%;
  margin: 0 auto 10px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 调整空隙大小 */
  margin-bottom: 20px;
}

</style>

