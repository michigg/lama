import Vue from 'vue'
import Vuex, { Module } from 'vuex'
import axios from 'axios'
import { IRootState } from '@/store/index'

export interface IGroupState {
  status: string
  loading: boolean
  error: boolean
  group: object
}

export const group: Module<IGroupState, IRootState> = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    group: {}
  },
  mutations: {
    SET_GROUP (state, { group }) {
      state.group = group
    },
    SET_LOADING_STATE (state, { loading, error }) {
      state.loading = loading
      state.error = error
    }
  },
  actions: {
    fetchGroup ({ dispatch, commit, rootState }, { realmId, groupDn }) {
      const url = rootState.config.lamaEndpoint.concat('/v1/realm/').concat(realmId).concat('/group/').concat(groupDn).concat('/')
      commit('SET_LOADING_STATE', { loading: true, error: false })
      axios.get(url)
        .then((response) => {
          commit('SET_GROUP', { group: response.data })
          commit('SET_LOADING_STATE', { loading: false, error: false })
        })
        .catch(() => {
          commit('SET_LOADING_STATE', { loading: false, error: true })
        })
    }
  },
  getters: {
    group: state => state.group
  },
  modules: {}
}
