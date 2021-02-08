import Vue from 'vue'
import Vuex from 'vuex'
import { store } from '@/apps/authentication/store'
import { realms } from '@/apps/realms/store/realms'
import { realm } from '@/apps/realms/store/realm'
import { users } from './users'
import { groups } from './groups'
import { user } from './user'
import { group } from './group'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    config: {
      loaded: false,
      lamaEndpoint: null
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
    authentication: store,
    realms: realms,
    realm: realm,
    users: users,
    user: user,
    groups: groups,
    group: group
  }
})
