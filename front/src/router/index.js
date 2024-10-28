import Vue from 'vue'
import VueRouter from "vue-router"

Vue.use(VueRouter)

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes: [
        {
            path:"/",
            name:"home",
            component:() => import("@/views/home.vue"),
        },
        {
            path:"/news",
            name:"news",
            component:() => import("@/views/news.vue"),
        },
        {
            path:"/login",
            name:"Login",
            component:() => import("@/views/login.vue"),
        },
        {
            path:"/user",
            name:"user",
            component:() => import("@/views/user.vue"),
        },
    ]
})

const originalPush = VueRouter.prototype.push;
const originalReplace = VueRouter.prototype.replace;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err);
};
VueRouter.prototype.replace = function replace(location) {
    return originalReplace.call(this, location).catch(err => err);
};

export default router