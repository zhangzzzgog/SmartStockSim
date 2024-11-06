<template>
  <el-row>
    <el-menu router
             :default-active="this.$route.path"
             mode="horizontal"
             style="font-weight: bold; font-size: 20px;"
             class="nav-menu"
             >
      <el-col span="24" style="margin-top: 10px; display: flex; justify-content: center; font-weight: normal; font-size: 16px;">
        <div class="current-time">{{ currentTime.replace(/\//g, '-') }}</div>
        <div>
        <span
            :style="{ color: marketStatusColor }"
            @click="showMarketTime"
            style="cursor: pointer;"
        >
          市场状态: {{ marketStatus }}
        </span>
        </div>
      </el-col>
      <el-col span="8" style="display: flex; justify-content: flex-start; align-items: center; ">
        <el-menu-item index="/" style="margin-left: 2vw">home</el-menu-item>
        <el-menu-item index="/news">news</el-menu-item>
      </el-col>
      <el-col span="8" style="display: flex; justify-content: center; "  >
        <div>
          <img  @click="goHome" class="stock-name-link" src="../assets/logo.svg" alt="logo" style="padding-top: 12px; color: #409EFF">
        </div>
        <span style="padding-top: 14px; padding-left: 10px; display: flex"  class="stock-name-link" @click="goHome">SmartStockSim</span>
      </el-col>
      <el-col span="8" style="display: flex; justify-content: flex-end; ">
        <div class="button-container">
          <span v-if="this.$store.state.isLogged" class="username">Hi! {{ this.$store.state.username }} </span>

          <button class="Btn" v-if="this.$store.state.isLogged" @click="logout()">
            <div class="sign">
              <svg viewBox="0 0 512 512">
                <path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"></path>
              </svg>
            </div>
            <div class="text">Logout</div>
          </button>

          <button class="Btn" v-if="!this.$store.state.isLogged" @click="goLogin()">
            <div class="sign">
              <svg viewBox="0 0 512 512">
                <path d="M217.9 105.9L340.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L217.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1L32 320c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM352 416l64 0c17.7 0 32-14.3 32-32l0-256c0-17.7-14.3-32-32-32l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64 0c53 0 96 43 96 96l0 256c0 53-43 96-96 96l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32z"></path>
              </svg>
            </div>
            <div class="text">Login</div>
          </button>

          <button class="Btn" @click="goUser()">
            <div class="sign">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 15 15">
                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
              </svg>
            </div>
            <div class="text">User</div>
          </button>
        </div>
      </el-col>

    </el-menu>
  </el-row>
</template>

<script>
export default {
  name: "navMenu",
  data(){
    return{
      currentTime: ''
    }
  },
  created() {
    this.$store.dispatch('loadUser');
    this.updateTime(); // 立即更新一次时间
    setInterval(this.updateTime, 1000); // 每秒更新
  },
  methods:{
    goHome() {
      this.$router.push({ path: `/` });
    },
    showMarketTime() {
      if (this.marketStatus === "开市") {
        this.$message({
          message: '开市时间范围: 上午9:35到11:30，下午1:05到3:00',
          type: 'success'
        });
      } else {
        this.$message({
          message: '开市时间范围: 上午9:35到11:30，下午1:05到3:00',
          type: 'info'
        });
      }
    }
,
    logout(){
      if(confirm("Are you sure you want to logout?")){
        this.$store.commit('logout');
      }
    },
    goLogin(){
      this.$router.push('/login');
    },
    goUser(){
      this.$router.push('/user')
    },
    updateTime() {
      const now = new Date();
      this.currentTime = now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
      console.log("Current Time:", this.currentTime); // 调试输出
    },
  }

,
  computed: {
    marketStatus() {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const currentTime = hours * 60 + minutes;

      const marketOpenMorning = 9 * 60 + 35;
      const marketCloseMorning = 11 * 60 + 30;
      const marketOpenAfternoon = 13 * 60 + 5;
      const marketCloseAfternoon = 15 * 60;

      if ((currentTime >= marketOpenMorning && currentTime <= marketCloseMorning) ||
          (currentTime >= marketOpenAfternoon && currentTime < marketCloseAfternoon)) {
        return "上市";
      } else {
        return "休市";
      }
    },
    marketStatusColor() {
      return this.marketStatus === "上市" ? "red" : "blue";
    }
  }
}
</script>


<style scoped>
.nav-menu{
  position: fixed; /* 固定位置 */
  top: 0; /* 距离顶部 0 */
  left: 0; /* 距离左边 0 */
  z-index: 1000; /* 确保菜单在最上层 */
  width: 100%; /* 宽度占满屏幕 */
}

.el-dropdown-menu__item, .el-menu-item{
  padding: 0 30px;
}

.el-menu.el-menu--horizontal .el-menu-item.is-active {
  border-bottom: 2px solid #409EFF;
}

.button-container {
  display: flex;
  height: 40px;
  align-items: center;
  justify-content: space-around;
  margin-top: 7px;
}

.icon {
  font-size: 20px;
}

.username{
  font-size: 16px;
  font-weight: normal;
  margin-right: 25px;
}

.Btn {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 50%;
  margin-right: 25px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition-duration: .3s;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.199);
  background-color: rgb(255, 255, 255);
}

/* plus sign */
.sign {
  width: 100%;
  transition-duration: .3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sign svg {
  width: 14px;
}

.sign svg path {
  fill: #409EFF;
}

.no-color{
  fill: none !important;
}

/* text */
.text {
  position: absolute;
  right: 0;
  width: 0;
  opacity: 0;
  color: #409EFF;
  font-size: 14px;
  font-weight: bold;
  font-family: Manrope;
  transition-duration: .3s;
}
/* hover effect on button width */
.Btn:hover {
  width: 105px;
  border-radius: 40px;
  transition-duration: .3s;
}

.Btn:hover .sign {
  width: 30%;
  transition-duration: .3s;
  padding-left: 5px;
}
/* hover effect button's text */
.Btn:hover .text {
  opacity: 1;
  width: 70%;
  transition-duration: .3s;
  padding-right: 5px;
}
/* button click effect*/
.Btn:active {
  transform: translate(2px ,2px);
}
.stock-name-link {
  color: #409EFF;
  cursor: pointer;
}

.current-time{
  margin-right: 20px;
}
</style>