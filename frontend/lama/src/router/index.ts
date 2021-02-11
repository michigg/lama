import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { store } from '@/store'
import Realms from '@/apps/realms/views/Realms.vue'
import PermissionDenied from '@/views/PermissionDenied.vue'
import Groups from '@/views/group/Groups.vue'
import Users from '@/apps/users/views/Users.vue'
import User from '@/apps/users/views/User.vue'
import Group from '@/views/group/Group.vue'
import { authenticationRoutes } from '@/apps/authentication/routes'
import CreateRealm from '@/apps/realms/views/CreateRealm.vue'
import Realm from '@/apps/realms/views/Realm.vue'

// let routes: Array<RouteRecordRaw> = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Realms,
//     meta: {
//       requiresAuth: true,
//       resource: 'Realm',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm',
//     name: 'Realms',
//     component: Realms,
//     meta: {
//       requiresAuth: true,
//       resource: 'Realm',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm-add',
//     name: 'CreateRealms',
//     component: CreateRealm,
//     meta: {
//       requiresAuth: true,
//       resource: 'Realm',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm/:realmId',
//     name: 'Realm',
//     component: Realm,
//     meta: {
//       requiresAuth: true,
//       resource: 'Realm',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm/:realmId/group',
//     name: 'Groups',
//     component: Groups,
//     meta: {
//       requiresAuth: true,
//       resource: 'Ldapgroup',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm/:realmId/group/:groupDn',
//     name: 'Group',
//     component: Group,
//     meta: {
//       requiresAuth: true,
//       resource: 'Ldapgroup',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm/:realmId/user',
//     name: 'Users',
//     component: Users,
//     meta: {
//       requiresAuth: true,
//       resource: 'Ldapuser',
//       action: 'view'
//     }
//   },
//   {
//     path: '/realm/:realmId/user/:userDn',
//     name: 'User',
//     component: User,
//     meta: {
//       requiresAuth: true,
//       resource: 'Ldapuser',
//       action: 'view'
//     }
//   },
//   {
//     path: '/permission-denied',
//     name: 'PermissionDenied',
//     component: PermissionDenied
//   },
//   {
//     path: '/about',
//     name: 'About',
//     // route level code-splitting
//     // this generates a separate chunk (about.[hash].js) for this route
//     // which is lazy-loaded when the route is visited.
//     component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
//   }
// ]
const routes = [...authenticationRoutes]

export const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
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
