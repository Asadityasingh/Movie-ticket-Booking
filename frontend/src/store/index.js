// store.js

import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    token: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      const response = await axios.post('/login', {
        username: credentials.username,
        password: credentials.password,
      });

      const token = response.data.access_token;

      commit('setToken', token);

      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      return token;
    },
  },
  getters: {
    isAuthenticated: (state) => state.token !== null,
  },
});

