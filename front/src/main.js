import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import '@/assets/font/font.css'

import elementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(elementUI);

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
