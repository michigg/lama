import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import Axios from 'axios'
import VueAxios from 'vue-axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueAxios, Axios)

const token = localStorage.getItem('token')
if (token) {
  Vue.axios.defaults.headers.common.Authorization = token
}

const getRuntimeConfig = async () => {
  const runtimeConfig = await fetch('/config/config.json')
  return await runtimeConfig.json()
}

getRuntimeConfig().then(function (json) {
  store.dispatch('initConfig', { lamaEndpoint: json.LAMA_ENDPOINT }).then()

  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app')
})
