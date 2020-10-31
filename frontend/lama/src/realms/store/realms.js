import Vue from 'vue'
import Vuex from 'vuex'
import RepositoryFactory from '@/authentication/repositories/RepositoryFactory'

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
        error: false
      })
      try {
        const realms = await RealmsRepository.getRealms()
        commit('SET_REALMS', { realms: realms })
        commit('SET_LOADING_STATE', {
          loading: false,
          error: false
        })
      } catch (error) {
        // TODO: improve error response
        commit('SET_LOADING_STATE', {
          loading: false,
          error: true
        })
      }
    }
  },
  getters: {
    realms: state => state.realms
  },
  modules: {}
}
