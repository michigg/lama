import { Ability, RawRuleOf } from '@casl/ability'
import { AuthenticationEndpoint } from '../api/lama'
import { AuthRepositoryException } from '../exceptions/repository'
import httpClient, { HttpClient } from '@/apps/authentication/clients/httpClient'
import { AuthTokenClient, authTokenClient } from '../clients/tokenClient'
import { User } from '@/apps/authentication/models/user'
import { Token } from '@/apps/authentication/models/token'

class AuthRepository {
  private httpClient: HttpClient
  private tokenClient: AuthTokenClient
  private user: User
  private readonly ability: Ability

  constructor () {
    this.ability = new Ability([])
    this.user = this.getEmptyUser()
    this.httpClient = httpClient
    this.tokenClient = authTokenClient
  }

  async login (username: string, password: string) {
    console.info('AUTH REPO: login')
    try {
      const response = await this.httpClient.client.post(AuthenticationEndpoint.Token, {
        username: username,
        password: password
      })
      return await this.initializeAuthenticationComponents(response.data)
    } catch (error) {
      this.user = this.getEmptyUser()
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
    if (this.user.isEmpty()) {
      const token = await this.tokenClient.getToken()
      if (!token.isEmpty()) {
        return await this.initializeAuthenticationComponents(token)
      }
      this.user = this.getEmptyUser()
    }
    return this.user
  }

  async initializeAuthenticationComponents (token: Token) {
    console.info('AUTH REPO: initializeAuthenticationComponents')
    const savedToken = await this.tokenClient.saveToken({
      accessToken: token.accessToken,
      refreshToken: token.refreshToken
    })
    this.httpClient.setAuthorizationHeader(savedToken.accessToken)
    if (!savedToken.user) {
      return User.emptyUser()
    }
    this.ability.update(savedToken.user.rules)
    this.user = new User(savedToken.user.username, savedToken.user.email, this.ability, savedToken.sessionExpirationTime)
    return this.user
  }

  async logout () {
    console.info('AUTH REPO: logout')
    await this.clearAuthenticationComponents()
  }

  async isLoggedIn () {
    const token = await this.tokenClient.getToken()
    return !token.isEmpty()
  }

  async clearAuthenticationComponents () {
    this.httpClient.clearAuthorizationHeader()
    this.tokenClient.clearToken()
    this.user = this.getEmptyUser()
  }

  getAbility () {
    return this.ability
  }

  getEmptyUser () {
    return User.emptyUser()
  }
}

const authRepository = new AuthRepository()
export default authRepository
