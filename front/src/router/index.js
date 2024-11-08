import Vue from 'vue'
import VueRouter from "vue-router"
import { Message } from 'element-ui';
import store from '@/store/index.js';

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
            path:'/stock/:id',
            name:"stock",
            component:() => import("@/views/stock.vue"),
            meta:{
                requiresAuth: true
            },
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
            meta:{
                requiresAuth: true
            }
        },
    ]
})

router.beforeEach((to, from, next) => {
    if(to.matched.some(record => record.meta.requiresAuth)){
        if(!store.state.isLogged){
            Message({
                message: 'Please log in',
                type: 'warning',
            });
            next({
                path:'/login',
                query: { redirect: to.fullPath },
            });
        }
        else{
            next();
        }
    }
    else{
        next();
    }
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