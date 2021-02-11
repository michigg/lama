import RepositoryFactory from '@/apps/authentication/repositories/RepositoryFactory'
import { Realm } from '@/apps/realms/models/realm'
import { Module } from 'vuex'
import { IRootState } from '@/store'

const RealmRepository = RepositoryFactory.get('realm')

export interface IRealmState {
  status: string,
  loading: boolean,
  error: boolean,
  realm: Realm
}

export const realm: Module<IRealmState, IRootState> = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    realm: Realm.emptyRealm()
  },
  mutations: {
    SET_REALM (state: IRealmState, realm: Realm) {
      state.realm = realm
    },
    SET_LOADING_STATE (state: IRealmState, { loading, error }: {loading: boolean, error: boolean}) {
      state.loading = loading
      state.error = error
    }
  },
  actions: {
    async fetchRealm ({ commit }, { realmId }: {realmId: number}) {
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
          error: error.message
        })
      }
    }
  },
  getters: {
    realm: (state: IRealmState) => state.realm,
    loading: (state: IRealmState) => state.loading
  }
}
