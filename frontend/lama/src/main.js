import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { abilitiesPlugin, Can } from '@casl/vue'
import RepositoryFactory from '@/authentication/repositories/RepositoryFactory'

const AuthenticationRepository = RepositoryFactory.get('authentication')

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(abilitiesPlugin, AuthenticationRepository.getAbility())
Vue.component('Can', Can)

const getRuntimeConfig = async () => {
  const runtimeConfig = await fetch('/config/config.json')
  return await runtimeConfig.json()
}

let app
getRuntimeConfig().then(function (json) {
  store.dispatch('initConfig', { lamaEndpoint: json.LAMA_ENDPOINT })
  if (window.Cypress) {
    // only available during E2E tests
    window.__store__ = store
  }
  store.dispatch('authentication/loadUser').then(() => {
    if (!app) {
      app = new Vue({
        router,
        store,
        render: h => h(App)
      }).$mount('#app')
    }
  })
})
