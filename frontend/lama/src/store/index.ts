import { InjectionKey } from 'vue'
import { createStore, useStore as baseUseStore, Store } from 'vuex'
import { store as authentication } from '@/apps/authentication/store'
import { realms } from '@/apps/realms/store/realms'
import { realm } from '@/apps/realms/store/realm'
import { users } from './users'
import { groups } from './groups'
import { user } from './user'
import { group } from './group'

export interface IRootState {
  config: {
    loaded: boolean,
    lamaEndpoint: string
  }
}

export const key: InjectionKey<Store<IRootState>> = Symbol('Vuex Store')

export const store = createStore<IRootState>({
  state: {
    config: {
      loaded: false,
      lamaEndpoint: ''
    }
  },
  mutations: {
    initConfig (state, config) {
      state.config.lamaEndpoint = config.lamaEndpoint
      state.config.loaded = true
    }
  },
  actions: {
    initConfig ({ commit }, config) {
      commit('initConfig', config)
    }
  },
  getters: {
    config: state => state.config
  },
  modules: {
    authentication: authentication,
    realms: realms,
    realm: realm,
    users: users,
    user: user,
    groups: groups,
    group: group
  }
})

export function useStore () {
  return baseUseStore(key)
}
