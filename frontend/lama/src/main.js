import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from '@/store'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import Axios from 'axios'
import VueAxios from 'vue-axios'
import { abilitiesPlugin, Can } from '@casl/vue'
import RepositoryFactory from '@/authentication/repositories/RepositoryFactory'

const AuthenticationRepository = RepositoryFactory.get('authentication')
AuthenticationRepository.httpClient.tokenInvalidProcedureFunction = router.push({ name: 'Login' })

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueAxios, Axios)
Vue.use(abilitiesPlugin, AuthenticationRepository.getAbility())
Vue.component('Can', Can)

if (window.Cypress) {
  // only available during E2E tests
  window.__store__ = store
}

const getRuntimeConfig = async () => {
  const runtimeConfig = await fetch('/config/config.json')
  return await runtimeConfig.json()
}

getRuntimeConfig().then(function (json) {
  store.dispatch('initConfig', { lamaEndpoint: json.LAMA_ENDPOINT }).then()
  store.dispatch('authentication/fetchLocalUser').then(() => {
    new Vue({
      router,
      store,
      render: h => h(App)
    }).$mount('#app')
  })
})
