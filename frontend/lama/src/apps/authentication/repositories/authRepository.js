import { Ability } from '@casl/ability'
import { AuthenticationEnpoint } from '../api/lama'
import { AuthReposioryException } from '../exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { authTokenClient } from '../clients/tokenClient'

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
    try {
      const response = await this.#httpClient.client.post(AuthenticationEnpoint.Token, {
        username: username,
        password: password
      })
      return await this.initializeAuthenticationComponents(response.data)
    } catch (error) {
      this.#user = this.getEmptyUser()
      if (error.toString() === 'Error: Network Error') {
        throw new AuthReposioryException('Es konnte keine Verbindung zum Server hergestellt werden. Bitte versuchen sie es später noch einmal.')
      } else {
        if (error.response.status === 401) {
          throw new AuthReposioryException('Fehlerhafter Nutzername oder fehlerhaftes Passwort')
        } else {
          throw new AuthReposioryException('Es ist ein unbekannter Fehler aufgetreten. Bitte versuchen sie es später erneut.')
        }
      }
    }
  }

  async loadUser () {
    if (this.#user.isEmpty()) {
      const token = await this.#tokenClient.getToken()
      if (!token.isEmpty()) {
        return await this.initializeAuthenticationComponents({
          access: token.accessToken,
          refresh: token.refreshToken
        })
      }
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

export class User {
  constructor (username, email, ability, sessionExpirationTime) {
    this.username = username
    this.email = email
    this.ability = ability
    this.sessionExpirationTime = sessionExpirationTime
  }

  isEmpty () {
    return !this.username
  }
}

const authRepository = new AuthRepository()
export default authRepository
