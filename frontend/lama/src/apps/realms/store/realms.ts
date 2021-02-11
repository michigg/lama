import { Module } from 'vuex'
import RepositoryFactory from '@/apps/authentication/repositories/RepositoryFactory'
import { Realm } from '@/apps/realms/models/realm'
import { IRootState } from '@/store'

const RealmsRepository = RepositoryFactory.get('realms')

export interface IRealmsState {
  status: string,
  loading: boolean,
  error: boolean,
  realms: Array<Realm>
}

export const realms: Module<IRealmsState, IRootState> = {
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
