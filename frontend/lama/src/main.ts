import Vue from 'vue'
import App from './App.vue'
import { key, store } from './store'
import { router } from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { abilitiesPlugin, Can } from '@casl/vue'
import RepositoryFactory from '@/apps/authentication/repositories/RepositoryFactory'

const AuthenticationRepository = RepositoryFactory.get('authentication')

const getRuntimeConfig = async () => {
  const runtimeConfig = await fetch('/config/config.json')
  return await runtimeConfig.json()
}

declare global {
  interface Window {
    Cypress: any
    __store__: any
  }
}

function runApp () {
  const app = Vue.createApp(App)
  app.use(router)
  app.use(store, key)
  app.use(BootstrapVue)
  app.use(IconsPlugin)
  app.use(abilitiesPlugin, AuthenticationRepository.getAbility(), { useGlobalProperties: true })
  app.component('Can', Can)
  app.mount('#app')
}

async function start () {
  try {
    const configJson = await getRuntimeConfig()
    await store.dispatch('initConfig', { lamaEndpoint: configJson.LAMA_ENDPOINT })
    if (window.Cypress) {
      // only available during E2E tests
      window.__store__ = store
    }
    await store.dispatch('authentication/loadUser')
    console.info('MAIN: User loaded')
    console.info('MAIN: RUN APP')
  } catch (error) {
    console.error(error)
  }
  runApp()
}

start().then()
