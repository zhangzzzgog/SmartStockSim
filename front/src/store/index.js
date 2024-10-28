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
        Login({ commit }, { username, password } ) {
            return new Promise((resolve, reject) => {
                login(username, password).then(response => {
                    localStorage.setItem('token', response.data.token);
                    commit('setLogin', username);
                    resolve();
                }).catch(error => {
                    reject(error);
                })
            })
        }
    }
})