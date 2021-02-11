import axios from 'axios'
import { Module } from 'vuex'
import { IRootState } from '@/store/index'
import { User } from '@/apps/users/models/user'

export interface IUserState {
  status: string
  loading: boolean
  error: boolean
  user: User
}

export const user: Module<IUserState, IRootState> = {
  namespaced: true,
  state: {
    status: '',
    loading: false,
    error: false,
    user: User.emptyUser()
  },
  mutations: {
    SET_USER (state, { user }) {
      state.user = user
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
    fetchUser ({
      dispatch,
      commit,
      rootState
    }, {
      realmId,
      userDn
    }) {
      const url = rootState.config.lamaEndpoint.concat('/v1/realm/').concat(realmId).concat('/user/').concat(userDn).concat('/')
      commit('SET_LOADING_STATE', {
        loading: true,
        error: false
      })
      axios.get(url)
        .then((response) => {
          commit('SET_USER', { user: response.data })
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
    user: state => state.user
  },
  modules: {}
}
