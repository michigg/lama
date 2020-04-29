import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const realm = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    realm: {}
  },
  mutations: {
    SET_REALM (state, { realm }) {
      state.realm = realm
    },
    SET_LOADING_STATE (state, { loading, error }) {
      state.loading = loading
      state.error = error
    }
  },
  actions: {
    fetchRealm ({ dispatch, commit, rootState }, { realmId }) {
      const url = rootState.config.lamaEndpoint.concat('/v1/realm/').concat(realmId).concat('/')
      commit('SET_LOADING_STATE', {
        loading: true,
        error: false
      })
      axios.get(url)
        .then((response) => {
          commit('SET_REALM', { realm: response.data })
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
    realm: state => state.realm,
    loading: state => state.loading
  },
  modules: {}
}
