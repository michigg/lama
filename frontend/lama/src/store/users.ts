import axios from 'axios'
import { Module } from 'vuex'
import { IRootState } from '@/store/index'
import { User } from '@/apps/users/models/user'

export interface IUsersState {
  status: string
  loading: boolean
  error: boolean
  users: Array<User>
}

export const users: Module<IUsersState, IRootState> = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    users: []
  },
  mutations: {
    SET_USERS (state, { users }) {
      state.users = users
    },
    SET_LOADING_STATE (state, {
      loading,
      error
    }) {
      state.loading = loading
      state.error = error
    }
  },
  actions: {
    fetchUsers ({
      dispatch,
      commit,
      rootState
    }, { realmId }) {
      const url = rootState.config.lamaEndpoint.concat('/v1/realm/').concat(realmId).concat('/user/')
      commit('SET_LOADING_STATE', {
        loading: true,
        error: false
      })
      axios.get(url)
        .then((response) => {
          commit('SET_USERS', { users: response.data.results })
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
    users: state => state.users
  },
  modules: {}
}
