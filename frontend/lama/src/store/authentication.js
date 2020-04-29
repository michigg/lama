import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import jwtDecode from 'jwt-decode'
import router from '../router/index'
import { Ability } from '@casl/ability'

Vue.use(Vuex)

export const ability = new Ability()

export const abilityPlugin = (store) => {
  ability.update(store.state.authentication.user.rules)
  return store.subscribe((mutation) => {
    if (mutation.type === 'SET_USER') {
      ability.update(mutation.payload.rules)
    }
  })
}

export const authentication = {
  namespaced: true,
  state: {
    status: '',
    token: {
      access: '',
      refresh: '',
      expire: -1
    },
    user: {
      username: '',
      rules: [],
      email: ''
    }
  },
  plugins: [abilityPlugin],
  mutations: {
    SET_JWT (state, { accessToken, refreshToken, expire }) {
      state.token.access = accessToken
      state.token.refresh = refreshToken
      state.token.expire = expire
    },
    SET_USER (state, { username, email, rules }) {
      console.log('SET USER')
      state.user.username = username
      state.user.email = email
      state.user.rules = rules
      ability.update(rules)
    },
    AUTH_REQUEST (state) {
      state.status = 'loading'
    },
    AUTH_SUCCESS (state, token, user) {
      state.status = 'success'
    },
    AUTH_ERROR (state) {
      state.status = 'error'
    }
  },
  actions: {
    login ({ dispatch, commit, rootState }, user) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST')
        const url = rootState.config.lamaEndpoint.concat('/auth/token/')
        axios({
          url: url,
          data: user,
          method: 'POST'
        })
          .then(response => {
            console.log(response.data)
            const accessToken = response.data.access
            const refreshToken = response.data.refresh
            const decodedToken = jwtDecode(accessToken)
            console.log(decodedToken)
            // TODO: better handling in production
            commit('SET_JWT', {
              accessToken: accessToken,
              refreshToken: refreshToken,
              expire: decodedToken.exp
            })
            // TODO: set axios auth header
            commit('SET_USER', decodedToken.user)

            // TODO: set casl rules
            commit('AUTH_SUCCESS')
            router.push({ name: 'Home' })
          })
          .catch(err => {
            commit('AUTH_ERROR')
            reject(err)
          })
      })
    },
    logout ({ commit }) {
      commit('SET_JWT', {
        accessToken: '',
        refreshToken: '',
        expire: -1
      })
      commit('SET_USER', {
        username: '',
        email: '',
        rules: []
      })
    }
  },
  getters: {
    isLoggedIn: state => !!state.token.access,
    rules: state => state.user.rules
  },
  modules: {}
}
