import RepositoryFactory from '@/authentication/repositories/RepositoryFactory'

const RealmRepository = RepositoryFactory.get('realm')

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
    async fetchRealm ({ commit }, { realmId }) {
      commit('SET_LOADING_STATE', {
        loading: true,
        error: false
      })
      try {
        const realm = await RealmRepository.getRealm(realmId)
        commit('SET_REALM', { realm: realm })
        commit('SET_LOADING_STATE', {
          loading: false,
          error: false
        })
      } catch (error) {
        commit('SET_LOADING_STATE', {
          loading: false,
          error: true
        })
      }
    }
  },
  getters: {
    realm: state => state.realm,
    loading: state => state.loading
  }
}
