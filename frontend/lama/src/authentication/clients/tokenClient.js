import jwtDecode from 'jwt-decode'

class AuthTokenClient {
  #accessTokenKey
  #refreshTokenKey
  #token

  constructor () {
    this.#accessTokenKey = 'access_token'
    this.#refreshTokenKey = 'refresh_token'
    this.#token = this.getEmptyToken()
  }

  async saveToken ({ accessToken, refreshToken }) {
    if (accessToken) {
      localStorage.setItem(this.#accessTokenKey, accessToken)
      localStorage.setItem(this.#refreshTokenKey, refreshToken)
    }
    this.#token = await this.getToken()
    return this.#token
  }

  clearToken () {
    this.#token = this.getEmptyToken()
    localStorage.removeItem(this.#accessTokenKey)
    localStorage.removeItem(this.#refreshTokenKey)
  }

  async getToken () {
    if (this.#token.isEmpty()) {
      await this.loadToken
    }
    return this.#token
  }

  async loadToken () {
    const accessToken = localStorage.getItem(this.#accessTokenKey)
    const refreshToken = localStorage.getItem(this.#refreshTokenKey)
    if (accessToken) {
      try {
        const decodedToken = await jwtDecode(accessToken)
        return new Token(accessToken, refreshToken, decodedToken.user, new Date(decodedToken.exp))
      } catch (error) {
        // eslint-disable-next-line no-console
        console.error(error)
      }
    }
    return this.getEmptyToken()
  }

  getEmptyToken () {
    return new Token(null, null, null, new Date())
  }
}

export class Token {
  constructor (accessToken, refreshToken, user, expirationTime) {
    this.accessToken = accessToken
    this.refreshToken = refreshToken
    this.user = user
    this.sessionExpirationTime = expirationTime
  }

  isEmpty () {
    return !this.accessToken || !this.refreshToken
  }

  isExpired () {
    //  TODO: implement
    return this.isEmpty()
  }
}

export const authTokenClient = new AuthTokenClient()
