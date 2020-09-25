import axios from 'axios'
import AuthTokenService from './auth_token_service'

const AxiosExtraUtils = (
  function () {
    function _setResponseInterceptor (tokenApiEnpoint) {
      axios.interceptors.response.use(
        (response) => {
          return response
        },
        async (error) => {
          const originalRequest = error.config
          if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            const data = { refreshToken: AuthTokenService.getRefreshToken() }
            return axios.post(tokenApiEnpoint, data)
              .then(response => {
                if (response.status === 201) {
                  AuthTokenService.setToken(response.data)
                  axios.defaults.headers.common.Authorization = `Bearer ${AuthTokenService.getAccessToken()}`
                  return axios(originalRequest)
                }
              })
          }
          return Promise.reject(error)
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
