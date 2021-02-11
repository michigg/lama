import { router } from '@/router'
import RepositoryFactory from '@/apps/authentication/repositories/RepositoryFactory'
import { Ability } from '@casl/ability'
import { Module } from 'vuex'
import { IRootState } from '@/store'

const AuthenticationRepository = RepositoryFactory.get('authentication')

export interface IAccountState {
  user: {
    username: string,
    email: string,
    ability: Ability
  }
}

export const store: Module<IAccountState, IRootState> = {
  namespaced: true,
  state: {
    user: {
      username: '',
      email: '',
      ability: new Ability([])
    }
  },
  getters: {
    user: state => state.user,
    isLoggedIn: state => !!state.user.username
  },
  mutations: {
    SET_USER (state, {
      username,
      email,
      ability
    }) {
      state.user.username = username
      state.user.email = email
      state.user.ability = ability
    },
    INIT_USER (state) {
      state.user.username = ''
      state.user.email = ''
      state.user.ability = new Ability([])
    }
  },
  actions: {
    async login ({ commit }, {
      username,
      password
    }) {
      const user = await AuthenticationRepository.login(username, password)
      commit('SET_USER', user)
    },
    async loadUser ({
      commit,
      state
    }) {
      console.log('STORE: loadUser')
      const user = await AuthenticationRepository.loadUser()
      console.log('STORE: loadUser', user)
      if (!user.isEmpty()) {
        commit('SET_USER', user)
      } else if (!state.user.username) {
        commit('INIT_USER')
      }
    },
    async loginWithToken ({
      commit,
      dispatch
    }, token) {
      const user = await AuthenticationRepository.initializeAuthenticationComponents(token)
      commit('SET_USER', user)
    },
    async logout ({ commit }) {
      console.log('STORE: logout')
      await AuthenticationRepository.logout()
      commit('INIT_USER')
      await router.push({ name: 'Login' })
    }
  }
}
