import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import store from '../store/index'
import { ability } from '../store/authentication'
import Realm from '../views/realm/Realm'
import Realms from '../views/realm/Realms'
import PermissionDenied from '../views/PermissionDenied'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Realms,
    meta: {
      resource: 'Realm',
      action: 'view',
      hasPermission: () => ability.can('Realm', 'view')
    }
  },
  {
    path: '/realm',
    name: 'Realms',
    component: Realms,
    meta: {
      requiresAuth: true,
      hasPermission: () => ability.can('Realm', 'view')
    }
  },
  {
    path: '/realm/:realmId',
    name: 'Realm',
    component: Realm,
    meta: {
      requiresAuth: true,
      hasPermission: () => ability.can('Realm', 'view')
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/permission-denied',
    name: 'PermissionDenied',
    component: PermissionDenied
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
router.beforeEach((to, from, next) => {
  const canNavigate = to.matched.some(route => {
    if ('action' in route.meta && 'resource' in route.meta) {
      return ability.can(route.meta.action, route.meta.resource)
    } else {
      return true
    }
  })
  const authRequired = to.matched.some(record => record.meta.requiresAuth)
  const isLoggedIn = store.getters['authentication/isLoggedIn']

  if (authRequired && !isLoggedIn) {
    next({
      path: '/login',
      query: { redirect: to.path }
    })
    return
  }
  if (!canNavigate) {
    next({ path: '/permission-denied' })
    return
  }
  next()
})

export default router
