import Login from '@/apps/authentication/views/Login'
import ForgotPassword from '@/apps/authentication/views/ForgotPassword'
import ForgotPasswordConfirm from '@/apps/authentication/views/ForgotPasswordConfirm'

export default [
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
