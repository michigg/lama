import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index'
import Realm from '@/apps/realms/views/Realm'
import Realms from '../apps/realms/views/Realms'
import PermissionDenied from '@/views/PermissionDenied'
import Groups from '@/views/group/Groups'
import Users from '@/apps/users/views/Users'
import User from '@/apps/users/views/User'
import Group from '@/views/group/Group'
import authenticationRoutes from '@/apps/authentication/routes'
import CreateRealm from '@/apps/realms/views/CreateRealm'

Vue.use(VueRouter)

let routes = [
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
    path: '/realm-add',
    name: 'CreateRealms',
    component: CreateRealm,
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
routes = [...routes, ...authenticationRoutes]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
router.beforeEach((to, from, next) => {
  const canNavigate = to.matched.some(route => {
    if ('action' in route.meta && 'resource' in route.meta) {
      const ability = store.getters['authentication/user'].ability
      return ability.can(route.meta.action, route.meta.resource)
    } else {
      return true
    }
  })
  const authRequired = to.matched.some(record => record.meta.requiresAuth)
  if (authRequired && !store.getters['authentication/isLoggedIn']) {
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
