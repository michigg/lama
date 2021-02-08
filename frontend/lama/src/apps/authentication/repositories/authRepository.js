import { Ability } from '@casl/ability'
import { AuthenticationEndpoint } from '../api/lama'
import { AuthRepositoryException } from '../exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { authTokenClient } from '../clients/tokenClient'
import { User } from '@/apps/authentication/models/user'

class AuthRepository {
  #httpClient
  #tokenClient
  #user
  #ability

  constructor () {
    this.#ability = new Ability([])
    this.#user = this.getEmptyUser()
    this.#httpClient = httpClient
    this.#tokenClient = authTokenClient
  }

  async login (username, password) {
    console.info('AUTH REPO: login')
    try {
      const response = await this.#httpClient.client.post(AuthenticationEndpoint.Token, {
        username: username,
        password: password
      })
      return await this.initializeAuthenticationComponents(response.data)
    } catch (error) {
      this.#user = this.getEmptyUser()
      if (error.toString() === 'Error: Network Error') {
        throw new AuthRepositoryException('Es konnte keine Verbindung zum Server hergestellt werden. Bitte versuchen sie es später noch einmal.')
      } else {
        if (error.response.status === 401) {
          throw new AuthRepositoryException('Fehlerhafter Nutzername oder fehlerhaftes Passwort')
        } else {
          throw new AuthRepositoryException('Es ist ein unbekannter Fehler aufgetreten. Bitte versuchen sie es später erneut.')
        }
      }
    }
  }

  async loadUser () {
    console.info('AUTH REPO: loadUser')
    if (this.#user.isEmpty()) {
      console.log('AUTH REPO: loadUser: user empty')
      const token = await this.#tokenClient.getToken()
      console.log('AUTH REPO: loadUser:', token)
      if (!token.isEmpty()) {
        console.log('AUTH REPO: loadUser: initializeAuthenticationComponents')
        return await this.initializeAuthenticationComponents({
          access: token.accessToken,
          refresh: token.refreshToken
        })
      }
      console.log('AUTH REPO: loadUser: Token EMPTY')
      this.#user = this.getEmptyUser()
    }
    return this.#user
  }

  async initializeAuthenticationComponents ({ access: accessToken, refresh: refreshToken }) {
    const token = await this.#tokenClient.saveToken({
      accessToken,
      refreshToken
    })
    this.#httpClient.setAuthorizationHeader(token.accessToken)
    this.#ability.update(token.user.rules)
    this.#user = new User(token.user.username, token.user.email, this.#ability, token.sessionExpirationTime)
    return this.#user
  }

  async logout () {
    console.log('AUTH REPO: logout')
    await this.clearAuthenticationComponents()
  }

  async isLoggedIn () {
    const token = await this.#tokenClient.getToken()
    return !token.isEmpty()
  }

  async clearAuthenticationComponents () {
    this.#httpClient.clearAuthorizationHeader()
    this.#tokenClient.clearToken()
    this.#user = this.getEmptyUser()
  }

  getAbility () {
    return this.#ability
  }

  getEmptyUser () {
    return new User(null, null, this.#ability, new Date())
  }
}

const authRepository = new AuthRepository()
export default authRepository
