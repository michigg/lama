import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'
import { Ability } from '@casl/ability'
import { RepositoryFactory } from './repositories/RepositoryFactory'
console.log(RepositoryFactory)
const AuthenticationRepository = RepositoryFactory.get('authentication')

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

export const store = {
  namespaced: true,
  state: {
    loading: false,
    error: '',
    user: {
      username: '',
      rules: [],
      email: ''
    }
  },
  plugins: [abilityPlugin],
  mutations: {
    SET_USER (state, { username, email, rules }) {
      state.user.username = username
      state.user.email = email
      state.user.rules = rules
    },
    INIT_USER (state) {
      state.user.username = null
      state.user.email = null
      state.user.rules = []
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
    async login ({ dispatch, commit, rootState }, { username, password }) {
      commit('AUTH_LOADING')
      try {
        const user = await AuthenticationRepository.login(username, password)
        commit('SET_USER', user)
        commit('AUTH_SUCCESS')
        await router.push({ name: 'Realms' })
      } catch (error) {
        commit('AUTH_ERROR', { message: error.message })
      }
    },
    async logout ({ commit }) {
      await AuthenticationRepository.logout()
      commit('INIT_USER')
    },
    async resetPassword ({ dispatch, commit, rootState }, { email }) {
      await AuthenticationRepository.resetPassword(email)
    },
    async resetPasswordConfirm ({ dispatch, commit, rootState }, { uid, token, newPassword }) {
      await AuthenticationRepository.resetPasswordConfirm(uid, token, newPassword)
    },
    async changePassword ({ commit, rootState }, { password, newPassword }) {
      await AuthenticationRepository.changePassword(password, newPassword)
    },
    async fetchLocalUser ({ commit }) {
      commit('AUTH_LOADING')
      try {
        const user = await AuthenticationRepository.fetchLocalUser()
        commit('SET_USER', user)
        commit('AUTH_SUCCESS')
      } catch (error) {
        commit('AUTH_ERROR', { message: error.message })
      }
    }
  },
  getters: {
    userLoading: state => state.loading,
    loginError: state => state.error,
    user: state => state.user
  }
}
