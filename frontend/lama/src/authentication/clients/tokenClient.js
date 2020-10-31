class AuthTokenClient {
  #accessTokenKey
  #refreshTokenKey

  constructor () {
    this.#accessTokenKey = 'access_token'
    this.#refreshTokenKey = 'refresh_token'
  }

  setToken (token) {
    localStorage.setItem(this.#accessTokenKey, token.access)
    localStorage.setItem(this.#refreshTokenKey, token.refresh)
  }

  getAccessToken () {
    return localStorage.getItem(this.#accessTokenKey)
  }

  getRefreshToken () {
    return localStorage.getItem(this.#refreshTokenKey)
  }

  clearToken () {
    localStorage.removeItem(this.#accessTokenKey)
    localStorage.removeItem(this.#refreshTokenKey)
  }
}

const authTokenClient = new AuthTokenClient()
export default authTokenClient
