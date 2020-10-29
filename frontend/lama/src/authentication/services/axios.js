import axios from 'axios'
import AuthTokenService from './authentication_token'
import router from '../../router'

const AxiosExtraUtils = (
  function () {
    function _setResponseInterceptor (tokenApiEnpoint) {
      axios.interceptors.response.use(
        (response) => {
          return response
        },
        async (error) => {
          if (error.response.status !== 401) {
            return new Promise((resolve, reject) => {
              reject(error)
            })
          }

          // Logout user if token refresh didn't work or user is disabled
          if (error.config.url === '/api/token/refresh/' || error.response.message === 'Account is disabled.' || error.response.data.code === 'token_not_valid') {
            console.log('BREAK')
            AuthTokenService.clearToken()
            await router.push({ name: 'Login' })

            return new Promise((resolve, reject) => {
              reject(error)
            })
          }
          const originalRequest = error.config
          originalRequest._retry = true
          const data = { refresh: AuthTokenService.getRefreshToken() }
          return axios.post(tokenApiEnpoint, data)
            .then(response => {
              if (response.status === 200) {
                AuthTokenService.setToken(response.data)
                axios.defaults.headers.common.Authorization = `Bearer ${AuthTokenService.getAccessToken()}`
                return axios(originalRequest)
              }
            })
            .catch((error) => {
              Promise.reject(error)
            })
        })
    }
    function _setRequestInterceptor () {
      axios.interceptors.request.use(
        (config) => {
          // TODO: implement access token auto refresh
          const token = AuthTokenService.getAccessToken()
          if (token) {
            config.headers.Authorization = `Bearer ${AuthTokenService.getAccessToken()}`
          }
          config.headers['Content-Type'] = 'application/json'
          return config
        },
        (error) => {
          Promise.reject(error)
        }
      )
    }

    return {
      setRequestInterceptor: _setRequestInterceptor,
      setResponseInterceptor: _setResponseInterceptor
    }
  })()
export default AxiosExtraUtils
