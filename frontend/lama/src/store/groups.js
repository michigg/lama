import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const groups = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    groups: []
  },
  mutations: {
    SET_GROUPS (state, { groups }) {
      state.groups = groups
    },
    SET_LOADING_STATE (state, { loading, error }) {
      state.loading = loading
      state.error = error
    }
  },
  actions: {
    fetchGroups ({ dispatch, commit, rootState }, { realmId }) {
      const url = rootState.config.lamaEndpoint.concat('/v1/realm/').concat(realmId).concat('/group/')
      commit('SET_LOADING_STATE', { loading: true, error: false })
      axios.get(url)
        .then((response) => {
          commit('SET_GROUPS', { groups: response.data.results })
          commit('SET_LOADING_STATE', { loading: false, error: false })
        })
        .catch(() => {
          commit('SET_LOADING_STATE', { loading: false, error: true })
        })
    }
  },
  getters: {
    groups: state => state.groups
  },
  modules: {}
}
