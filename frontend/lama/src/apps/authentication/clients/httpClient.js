import axios from 'axios'
import { authTokenClient } from './tokenClient'
import { AuthenticationEndpoint } from '@/apps/authentication/api/lama'

import store from '@/store'

class HttpClient {
  constructor () {
    this.client = axios
    this.isAlreadyFetchingAccessToken = false
    this.subscribers = []
    this.setResponseInterceptor()
    this.client.defaults.headers['Content-Type'] = 'application/json'
  }

  clearAuthorizationHeader () {
    delete this.client.defaults.headers.common.Authorization
  }

  setAuthorizationHeader (accessToken) {
    if (accessToken) {
      this.client.defaults.headers.common.Authorization = `Bearer ${accessToken}`
    } else {
      this.clearAuthorizationHeader()
    }
  }

  setResponseInterceptor () {
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const errorResponse = error.response
        if (this.isTokenExpiredError(errorResponse)) {
          return this.resetTokenAndReattemptRequest(error)
        }
        return Promise.reject(error)
      })
  }

  isTokenExpiredError (errorResponse) {
    return errorResponse.data.code === 'token_not_valid'
  }

  async resetTokenAndReattemptRequest (error) {
    try {
      const { response: errorResponse } = error
      const token = await authTokenClient.getToken()
      if (token.isEmpty()) {
        console.log('HTTPCLIENT: Token is empty')
        // Refresh not possible
        return Promise.reject(error)
      }
      const retryOriginalRequest = new Promise((resolve, reject) => {
        this.addSubscriber(accessToken => {
          if (accessToken) {
            errorResponse.config.headers.Authorization = 'Bearer ' + accessToken
            resolve(this.client(errorResponse.config))
          } else {
            reject(error)
          }
        })
      })
      if (!this.isAlreadyFetchingAccessToken) {
        console.log('HTTPCLIENT: !isAlreadyFetchingAccessToken')
        this.isAlreadyFetchingAccessToken = true
        const data = { refresh: token.refreshToken }
        const response = await this.client.post(AuthenticationEndpoint.RefreshToken, data)
        if (!response.data) {
          return Promise.reject(error)
        }
        const newRawToken = response.data
        this.isAlreadyFetchingAccessToken = false
        await this.onAccessTokenFetched(newRawToken)
      }
      return retryOriginalRequest
    } catch (error) {
      console.log(error)
      await this.onAccessTokenFetchedFailed()

      return Promise.reject(error)
    }
  }

  async onAccessTokenFetched (rawToken) {
    const token = await authTokenClient.saveToken({
      accessToken: rawToken.access,
      refreshToken: rawToken.refresh
    })
    this.subscribers.forEach(callback => callback(token.accessToken))
    this.subscribers = []
    await store.dispatch('authentication/loginWithToken', token)
  }

  async onAccessTokenFetchedFailed () {
    this.subscribers.forEach(callback => callback(null))
    this.subscribers = []
    await store.dispatch('authentication/logout')
  }

  addSubscriber (callback) {
    this.subscribers.push(callback)
  }
}

const httpClient = new HttpClient()
export default httpClient
