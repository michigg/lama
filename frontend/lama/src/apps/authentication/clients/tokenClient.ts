import jwtDecode from 'jwt-decode'
import { Token } from '@/apps/authentication/models/token'
import { ApiTokenInterface, RawTokenInterface } from '@/apps/authentication/interfaces/token'

export class AuthTokenClient {
  private readonly ACCESS_TOKEN_KEY: string
  private readonly REFRESH_TOKEN_KEY: string
  private token: Token

  constructor () {
    this.ACCESS_TOKEN_KEY = 'access_token'
    this.REFRESH_TOKEN_KEY = 'refresh_token'
    this.token = this.getEmptyToken()
  }

  async saveToken ({
    accessToken,
    refreshToken
  }: RawTokenInterface) {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken)
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken)
    this.token = await this.getToken()
    return this.token
  }

  clearToken () {
    this.token = this.getEmptyToken()
    localStorage.removeItem(this.ACCESS_TOKEN_KEY)
    localStorage.removeItem(this.REFRESH_TOKEN_KEY)
  }

  async getToken () {
    if (this.token.isEmpty()) {
      this.token = await this.loadToken()
    }
    return this.token
  }

  async loadToken () {
    const accessToken = localStorage.getItem(this.ACCESS_TOKEN_KEY)
    const refreshToken = localStorage.getItem(this.REFRESH_TOKEN_KEY)
    if (accessToken && refreshToken) {
      try {
        const decodedToken = await jwtDecode<ApiTokenInterface>(accessToken)
        return new Token(accessToken, refreshToken, decodedToken.user, new Date(decodedToken.exp))
      } catch (error) {
        // eslint-disable-next-line no-console
        console.error(error)
      }
    }
    return this.getEmptyToken()
  }

  getEmptyToken () {
    return new Token('', '', null, new Date())
  }
}

export const authTokenClient = new AuthTokenClient()
