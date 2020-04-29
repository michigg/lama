import Vue from 'vue'
import Vuex from 'vuex'
import { authentication } from './authentication'

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
    authentication: authentication
  }
})
