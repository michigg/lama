import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import jwtDecode from 'jwt-decode'
import router from '../router/index'
import { Ability } from '@casl/ability'
import AuthTokenService from '../auth_token_service'
import AxiosExtraUtils from '../axios_tools'

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
    loading: false,
    error: '',
    token: {
      access: AuthTokenService.getAccessToken() || null,
      refresh: AuthTokenService.getRefreshToken() || null,
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
      AuthTokenService.setToken(state.token)
    },
    INIT_JWT (state) {
      state.token.access = null
      state.token.refresh = null
      AuthTokenService.clearToken()
    },
    SET_USER (state, { username, email, rules }) {
      state.user.username = username
      state.user.email = email
      state.user.rules = rules
      ability.update(rules)
    },
    INIT_USER (state) {
      state.user.username = null
      state.user.email = null
      state.user.rules = []
      ability.update([])
    },
    AUTH_LOADING (state) {
      state.error = ''
      state.loading = true
    },
    AUTH_SUCCESS (state) {
      state.loading = false
    },
    AUTH_ERROR (state, { message }) {
      state.error = message
      state.loading = false
    }
  },
  actions: {
    async login ({ dispatch, commit, rootState }, user) {
      commit('AUTH_LOADING')
      const url = rootState.config.lamaEndpoint.concat('/auth/token/')
      try {
        const response = await axios.post(url, user)
        const accessToken = response.data.access
        const refreshToken = response.data.refresh
        const decodedToken = jwtDecode(accessToken)
        commit('SET_JWT', {
          accessToken: accessToken,
          refreshToken: refreshToken,
          expire: decodedToken.exp
        })
        commit('SET_USER', decodedToken.user)
        AxiosExtraUtils.setRequestInterceptor()
        AxiosExtraUtils.setResponseInterceptor(url)
        // TODO: set casl rules
        commit('AUTH_SUCCESS')
        router.push({ name: 'Home' })
      } catch (error) {
        if (error.toString() === 'Error: Network Error') {
          commit('AUTH_ERROR', { message: 'Es konnte keine Verbindung zum Server hergestellt werden. Bitte versuchen sie es später noch einmal.' })
        } else {
          if (error.response.status === 401) {
            commit('AUTH_ERROR', { message: 'Fehlerhafter Nutzername oder fehlerhaftes Passwort' })
          } else {
            commit('AUTH_ERROR', { message: 'Es ist ein unbekannter Fehler aufgetreten. Bitte versuchen sie es später erneut.' })
          }
        }
      }
    },
    logout ({ commit }) {
      commit('INIT_JWT')
      commit('INIT_USER')
      delete axios.headers.common.Authorization
    },
    async resetPassword ({ dispatch, commit, rootState }, { email }) {
      const url = rootState.config.lamaEndpoint.concat('/auth/token/')
      await axios.post(url, { email: email })
    },
    async resetPasswordConfirm ({ dispatch, commit, rootState }, { uid, token, newPassword }) {
      const url = rootState.config.lamaEndpoint.concat('/auth/token/')
      await axios.post(url, {
        uid: uid,
        token: token,
        newPassword: newPassword
      })
    },
    async changePassword ({ commit, rootState }, { password, newPassword }) {
      const url = rootState.config.lamaEndpoint.concat('/auth/token/')
      await axios.post(url, {
        password: password,
        newPassword: newPassword
      })
    }
  },
  getters: {
    isLoggedIn: state => state.token.access,
    rules: state => state.user.rules,
    loginError: state => state.error
  }
}
