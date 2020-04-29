import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const realms = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    realms: []
  },
  mutations: {
    SET_REALMS (state, { realms }) {
      state.realms = realms
    },
    SET_LOADING_STATE (state, { loading, error }) {
      state.loading = loading
      state.error = error
    }
  },
  actions: {
    fetchRealms ({ dispatch, commit, rootState }, user) {
      const url = rootState.config.lamaEndpoint.concat('/v1/realm/')
      commit('SET_LOADING_STATE', {
        loading: true,
        error: false
      })
      axios.get(url)
        .then((response) => {
          commit('SET_REALMS', { realms: response.data.results })
          commit('SET_LOADING_STATE', {
            loading: false,
            error: false
          })
        })
        .catch(() => {
          commit('SET_LOADING_STATE', {
            loading: false,
            error: true
          })
        })
    }
  },
  getters: {
    realms: state => state.realms
  },
  modules: {}
}
