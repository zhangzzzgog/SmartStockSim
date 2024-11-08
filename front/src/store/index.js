import Vue from 'vue';
import Vuex from 'vuex';
import { login } from "@/api/login";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        username: null,
        isLogged: !!localStorage.getItem('token'),
    },
    mutations: {
        setLogin(state, user) {
            state.username = user;
            state.isLogged = true;
        },
        logout(state) {
            state.username = null;
            state.isLogged = false;
        }
    },

    actions: {
        loadUser({ commit }) {
            const token = localStorage.getItem('token');
            if (token) {
                // 假设你可以通过 token 获取用户名
                const username = localStorage.getItem('userName'); // 假设你也存储了用户名
                commit('setLogin', username);
            }
        },
        Login({ commit }, { username, password } ) {
            return new Promise((resolve, reject) => {
                login(username, password).then(response => {
                    localStorage.setItem('token', response.data.token);
                    localStorage.setItem('userName', response.data.userName);
                    commit('setLogin', username);
                    resolve();
                }).catch(error => {
                    reject(error);
                })
            })
        }
    }
})