<template>
  <div class="loginPage">
    <span @click="goBack" class="close-button">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
      </svg>
    </span>
    <div class="wrapper" v-if="ifLogin">
      <div class="input-data" style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Log in</h2>
        <span @click="changeLogin" class="change">
          -> Sign up
        </span>
      </div>
      <div class="input-data">
        <input
            type="text"
            v-model="username"
            @focus="focusedField = 'username'"
            @blur="focusedField = ''"
            :class="{ 'is-focused': focusedField === 'username', 'is-valid': username !== '' }"
        />
        <div class="underline"></div>
        <label :class="{ 'is-focused': focusedField === 'username', 'is-valid': username !== '' }">Username</label>
      </div>
      <div class="input-data">
        <input
            type="text"
            v-model="password"
            @focus="focusedField = 'password'"
            @blur="focusedField = ''"
            :class="{ 'is-focused': focusedField === 'password', 'is-valid': password !== '' }"
        />
        <div class="underline"></div>
        <label :class="{ 'is-focused': focusedField === 'password', 'is-valid': password !== '' }">Password</label>
      </div>
      <div class="input-data">
        <a href="#" class="login" @click="handleLogin()">Sign in</a>
      </div>
    </div>
    <div class="wrapper" v-if="!ifLogin">
      <div class="input-data" style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Sign up</h2>
        <span @click="changeLogin" class="change">
          -> Log in
        </span>
      </div>
      <div class="input-data">
        <input
            type="text"
            v-model="username"
            @focus="focusedField = 'username'"
            @blur="focusedField = ''"
            :class="{ 'is-focused': focusedField === 'username', 'is-valid': username !== '' }"
        />
        <div class="underline"></div>
        <label :class="{ 'is-focused': focusedField === 'username', 'is-valid': username !== '' }">Username</label>
      </div>
      <div class="input-data">
        <input
            type="text"
            v-model="password"
            @focus="focusedField = 'password'"
            @blur="focusedField = ''"
            :class="{ 'is-focused': focusedField === 'password', 'is-valid': password !== '' }"
        />
        <div class="underline"></div>
        <label :class="{ 'is-focused': focusedField === 'password', 'is-valid': password !== '' }">Password</label>
      </div>
      <div class="input-data">
        <a href="#" class="login" @click="handleRegister()">Create Account</a>
      </div>
    </div>
  </div>
</template>

<script>
import { register } from "@/api/login";

export default {
  name: 'loginPage',
  data(){
    return{
      ifLogin: true,
      focusedField: '',
      username: '',
      password: '',
      redirect: '', //路由
    }
  },
  methods:{
    handleLogin(){ //登录
      if(this.username.trim().length !== 0 && this.password.trim().length !== 0) {
        this.$store.dispatch("Login", {username: this.username, password: this.password} ).then(() => {
              this.$message.success("Login successful");
              this.$router.push({ path: this.redirect || "/" });
            }).catch((err) => {
              console.log(err);
              this.$message.error("invalid username or password");
            });
      }
      else{
        this.$message({
          message: 'Please enter your username and password',
          type: 'warning'
        });
      }
    },
    handleRegister(){ //注册
      if(this.username.trim().length !== 0 && this.password.trim().length !== 0) {
        register(this.username, this.password).then(() => {
          this.$message.success("Registration successful");
          this.changeLogin();
        }).catch((err) => {
          console.log(err);
        })
      }
    },
    changeLogin(){
      this.ifLogin = !this.ifLogin;
      this.username = '';
      this.password = '';
    },
    goBack(){
      this.$router.go(-1);
    },
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  outline: none;
  box-sizing: border-box;
  text-decoration: none;
}

.loginPage {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  /* body最小高度为100%窗口高度 */
  background: linear-gradient(200deg, #0c3483, #a2b6df);
  /* 设置渐变背景 */
}

.close-button {
  position: absolute;
  top: 5vh; /* 根据需要调整 */
  right: 5vw; /* 根据需要调整 */
  font-size: 16px;
  cursor: pointer;
  background: transparent;
  border: none;
}

.change {
  user-select: none;
  cursor: pointer;
  color: #548eff;
  font-weight: bold;
  &:hover{
    color: lightskyblue;
  }
}

.wrapper {
  width: 450px;
  background-color: #fff;
  padding: 40px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.wrapper .input-data {
  position: relative;
  width: 100%;
  height: 40px;
}

.wrapper .input-data input {
  width: 100%;
  height: 100%;
  border: none;
  font-size: 17px;
  border-bottom: 2px solid #c0c0c0;
}

/* 输入框获得焦点时，输入框的值合法时，label上移25px，改变字号和颜色 */
.wrapper .input-data input.is-focused~label,
.wrapper .input-data input.is-valid~label {
  transform: translateY(-25px);
  font-size: 15px;
  color: #2c6fdb;
}

.wrapper .input-data label {
  position: absolute;
  bottom: 10px;
  left: 0px;
  color: #808080;
  pointer-events: none;
  /* 动画过渡 */
  transition: all 0.3s ease;
}

.wrapper .input-data .underline {
  position: absolute;
  bottom: 0px;
  height: 2px;
  width: 100%;
  background-color: #2c6fdb;
  transform: scaleX(0);
  transition: all 0.3s ease;
}

.wrapper .input-data input.is-focused~.underline,
.wrapper .input-data input.is-valid~.underline {
  transform: scaleX(1);
}

.wrapper .input-data:nth-child(1) {
  margin-bottom: 25px;
}

.wrapper .input-data:nth-child(2) {
  margin-bottom: 30px;
}

.wrapper .input-data:nth-child(3) {
  margin-bottom: 40px;
}

.wrapper .input-data:nth-child(4) {
  border: 1px solid #c0c0c0;
  border-radius: 4px;
}

.wrapper .input-data .login {
  display: flex;
  text-align: center;
  height: 39px;
  justify-content: center;
  align-items: center;
}

.wrapper .input-data a:link {
  color: #808080;
}

.wrapper .input-data a:visited {
  color: #808080;
}

.wrapper .input-data a:hover {
  color: #fff;
  background-color: #c0c0c0;
}

.wrapper .input-data a:active {
  color: #808080;
}
</style>