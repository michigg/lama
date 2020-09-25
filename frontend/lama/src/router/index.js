import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/auth/Login.vue'
import store from '../store/index'
import { ability } from '../store/authentication'
import Realm from '../views/realm/Realm'
import Realms from '../views/realm/Realms'
import PermissionDenied from '../views/PermissionDenied'
import Groups from '../views/group/Groups'
import Users from '../views/user/Users'
import User from '../views/user/User'
import Group from '../views/group/Group'
import ForgotPassword from '../views/auth/ForgotPassword'
import ForgotPasswordConfirm from '../views/auth/ForgotPasswordConfirm'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Realms,
    meta: {
      requiresAuth: true,
      resource: 'Realm',
      action: 'view'
    }
  },
  {
    path: '/realm',
    name: 'Realms',
    component: Realms,
    meta: {
      requiresAuth: true,
      resource: 'Realm',
      action: 'view'
    }
  },
  {
    path: '/realm/:realmId',
    name: 'Realm',
    component: Realm,
    meta: {
      requiresAuth: true,
      resource: 'Realm',
      action: 'view'
    }
  },
  {
    path: '/realm/:realmId/group',
    name: 'Groups',
    component: Groups,
    meta: {
      requiresAuth: true,
      resource: 'Ldapgroup',
      action: 'view'
    }
  },
  {
    path: '/realm/:realmId/group/:groupDn',
    name: 'Group',
    component: Group,
    meta: {
      requiresAuth: true,
      resource: 'Ldapgroup',
      action: 'view'
    }
  },
  {
    path: '/realm/:realmId/user',
    name: 'Users',
    component: Users,
    meta: {
      requiresAuth: true,
      resource: 'Ldapuser',
      action: 'view'
    }
  },
  {
    path: '/realm/:realmId/user/:userDn',
    name: 'User',
    component: User,
    meta: {
      requiresAuth: true,
      resource: 'Ldapuser',
      action: 'view'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword
  },
  {
    path: '/forgot-password-confirm',
    name: 'ForgotPasswordConfirm',
    component: ForgotPasswordConfirm
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
