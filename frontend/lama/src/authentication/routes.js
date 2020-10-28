import Login from '@/authentication/views/Login'
import ForgotPassword from '@/authentication/views/ForgotPassword'
import ForgotPasswordConfirm from '@/authentication/views/ForgotPasswordConfirm'

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
