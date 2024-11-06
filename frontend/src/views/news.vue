<template>
  <div>
    <nav-menu></nav-menu>
    <p style="text-align: center; font-size: 24px; margin-bottom: 20px; letter-spacing: 1px"> News </p>
    <el-divider>
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-newspaper" viewBox="0 0 16 16">
        <path d="M0 2.5A1.5 1.5 0 0 1 1.5 1h11A1.5 1.5 0 0 1 14 2.5v10.528c0 .3-.05.654-.238.972h.738a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 1 1 0v9a1.5 1.5 0 0 1-1.5 1.5H1.497A1.497 1.497 0 0 1 0 13.5v-11zM12 14c.37 0 .654-.211.853-.441.092-.106.147-.279.147-.531V2.5a.5.5 0 0 0-.5-.5h-11a.5.5 0 0 0-.5.5v11c0 .278.223.5.497.5H12z"/>
        <path d="M2 3h10v2H2V3zm0 3h4v3H2V6zm0 4h4v1H2v-1zm0 2h4v1H2v-1zm5-6h2v1H7V6zm3 0h2v1h-2V6zM7 8h2v1H7V8zm3 0h2v1h-2V8zm-3 2h2v1H7v-1zm3 0h2v1h-2v-1zm-3 2h2v1H7v-1zm3 0h2v1h-2v-1z"/>
      </svg>
    </el-divider>

    <!-- 条件搜索 -->
    <div class="search-container" >
      <el-input @current-change="handleCurrentChange" placeholder="输入新闻标题" v-model="title" style="width: 250px; margin-right: 40px;"></el-input>
      <el-date-picker @current-change="handleCurrentChange" v-model="startDate" type="date" placeholder="开始日期" style="margin-right: 40px;"></el-date-picker>
      <el-date-picker @current-change="handleCurrentChange" v-model="endDate" type="date" placeholder="结束日期" style="margin-right: 20px;"></el-date-picker>
      <el-button type="primary"  @click="searchNews">搜索</el-button>
    </div>

    <div class="news-div">
      <span v-for="article in paginatedArticles" :key="article.title">
        <news-card :article="article"></news-card>
      </span>
    </div>

    <div class="pagination-container">
      <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :total="filteredArticles.length"
          @current-change="handleCurrentChange"
          layout="total, prev, pager, next"
      />
    </div>
  </div>

</template>

<script>
import navMenu from "@/components/navmenu.vue";
import newsCard from "@/components/newsCard.vue";
import { newsList } from "@/api/news"

export default {
  name: "newsPage",
  components: {
    'nav-menu': navMenu,
    'news-card': newsCard,
  },
  data() {
    return {
      articles: [],
      filteredArticles: [],
      startDate: localStorage.getItem('startDate')&&localStorage.getItem('startDate')!=='null' ? new Date(localStorage.getItem('startDate')) : null,
      endDate: localStorage.getItem('endDate')&&localStorage.getItem('endDate')!=='null' ? new Date(localStorage.getItem('endDate')) : null,
      title: localStorage.getItem('title')&&localStorage.getItem('title')!=='null'? localStorage.getItem('title') :null,
      currentPage: localStorage.getItem('currentPage')&&localStorage.getItem('currentPage')!=='null'?Number(localStorage.getItem('currentPage')):1 ,
      pageSize: 9,
    }
  },
  created() {
    this.searchNews();
  },
  methods: {
    getNewsList() {
      return newsList().then(res => {
        this.articles = res.data.news;
        this.filteredArticles = this.articles; // 初始化时将所有文章存储
      });
    },
    searchNews() {
      this.getNewsList().then(() => {
        this.filteredArticles = this.articles.filter(article => {
          const articleDate = new Date(article.publishedAt);
          const isInDateRange = (!this.startDate || articleDate >= new Date(this.startDate)) &&
              (!this.endDate || articleDate <= new Date(this.endDate));
          const isTitleMatch = this.title ? article.title.includes(this.title) : true;
          return isInDateRange && isTitleMatch;
        });
        this.saveSearchParams();

      });
    },
    handleCurrentChange(page) {
      this.currentPage = page;
      this.saveSearchParams();
    },
    saveSearchParams() {
      localStorage.setItem('startDate', this.startDate ? this.startDate.toISOString() : null);
      localStorage.setItem('endDate', this.endDate ? this.endDate.toISOString() : null);
      localStorage.setItem('title', this.title);
      localStorage.setItem('currentPage', this.currentPage);
    }
  },

  computed: {
    paginatedArticles() {
      const start = (this.currentPage - 1) * this.pageSize;
      return this.filteredArticles.slice(start, start + this.pageSize);
    }
  }
}
</script>

<style scoped>
.news-div {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.search-container {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 和新闻保持间距 */
}
.el-divider {
  background-color: #89c4fd;
  height: 1.2px;
  width: 80%;
  margin: 0 auto 10px;
}
</style>
