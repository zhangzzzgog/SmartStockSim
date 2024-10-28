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
    <div class="news-div">
      <span v-for="article in articles" :key="article.title">
        <news-card :article="article"></news-card>
      </span>
      <news-card :article="article" style="visibility: hidden;"></news-card>
      <news-card :article="article" style="visibility: hidden;"></news-card>
      <news-card :article="article" style="visibility: hidden;"></news-card>
      <news-card :article="article" style="visibility: hidden;"></news-card>
      <news-card :article="article" style="visibility: hidden;"></news-card>
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
      articles: [{
        title: 'new1',
        description: '123456789',
        publishedAt: '1234-56-78',
        detail:'xijie'
      }, {
        title: 'new2',
        description: '123456789',
        publishedAt: '1234-56-78',
        detail:'xijie'
      }, {
        title: 'news3',
        description: '123456789',
        publishedAt: '1234-56-78',
        detail:'xijie'
      }],
    }
  },
  created() {
    this.getNewsList();
  },
  methods: {
    getNewsList(){
      newsList().then(res => {
        this.articles = res.data.news;
      })
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
.el-divider{
  background-color: #89c4fd;
  height: 1.2px;
  width: 80%;
  margin: 0 auto 10px;
}
</style>