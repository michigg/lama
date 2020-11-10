import Vue from 'vue'
import Vuex from 'vuex'
import RepositoryFactory from '@/apps/authentication/repositories/RepositoryFactory'

const RealmsRepository = RepositoryFactory.get('realms')

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
    async fetchRealms ({ commit }, user) {
      commit('SET_LOADING_STATE', {
        loading: true,
        error: null
      })
      try {
        const realms = await RealmsRepository.getRealms()
        commit('SET_REALMS', { realms: realms })
        commit('SET_LOADING_STATE', {
          loading: false,
          error: null
        })
      } catch (error) {
        // TODO: improve error response
        commit('SET_LOADING_STATE', {
          loading: false,
          error: error.message
        })
      }
    }
  },
  getters: {
    realms: state => state.realms,
    loading: state => state.loading,
    error: state => state.error
  },
  modules: {}
}
