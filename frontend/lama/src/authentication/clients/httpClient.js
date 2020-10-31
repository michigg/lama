import axios from 'axios'
import AuthTokenService from '../clients/tokenClient'

// import router from '../../router'

class HttpClient {
  constructor () {
    this.client = axios
    this.tokenInvalidProcedureFunction = null
  }

  setRequestInterceptor () {
    this.client.interceptors.request.use(
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
        return Promise.reject(error)
      }
    )
  }

  setResponseInterceptor (tokenApiEndpoint) {
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response.status !== 401) {
          return Promise.reject(error)
        }

        // Logout user if token refresh didn't work or user is disabled
        if (error.config.url === '/api/token/refresh/' || error.response.data.code === 'token_not_valid') {
          AuthTokenService.clearToken()
          if (this.tokenInvalidProcedureFunction) {
            await this.tokenInvalidProcedureFunction()
          }

          return Promise.reject(error)
        }
        return await this.refreshLogin(error, error.config, tokenApiEndpoint)
      })
  }

  async refreshLogin (originalError, originalRequest, tokenApiEndpoint) {
    originalRequest._retry = true
    const data = { refresh: AuthTokenService.getRefreshToken() }
    try {
      const response = await this.client.post(tokenApiEndpoint, data)
      if (response.status === 200) {
        AuthTokenService.setToken(response.data)
        this.client.defaults.headers.common.Authorization = `Bearer ${AuthTokenService.getAccessToken()}`
        return this.client(originalRequest)
      } else {
        return Promise.reject(originalError)
      }
    } catch (error) {
      return Promise.reject(error)
    }
  }

  clearAuthorizationHeader () {
    delete this.client.defaults.headers.common.Authorization
  }
}

const httpClient = new HttpClient()
export default httpClient
