import Login from '@/apps/authentication/views/Login.vue'
import ForgotPassword from '@/apps/authentication/views/ForgotPassword.vue'
import ForgotPasswordConfirm from '@/apps/authentication/views/ForgotPasswordConfirm.vue'
import { RouteRecordRaw } from 'vue-router'

export const authenticationRoutes: Array<RouteRecordRaw> = [
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
  }
]
