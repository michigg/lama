import jwtDecode from 'jwt-decode'
import AuthTokenService from '../clients/tokenClient'
import { Ability } from '@casl/ability'
import { AuthenticationEnpoint } from '../api/lama'
import { AuthReposioryException } from '../exceptions/repository'
import httpClient from '@/authentication/clients/httpClient'

class AuthRepository {
  constructor () {
    this.ability = new Ability()
    this.httpClient = httpClient
  }

  async isLoggedIn () {
    return !!AuthTokenService.getAccessToken()
  }

  async fetchLocalUser () {
    const token = AuthTokenService.getAccessToken()
    if (token) {
      const decodedToken = jwtDecode(token)
      await this.initializeAuthenticationComponents(decodedToken)
      return decodedToken.user
    } else {
      return {}
    }
  }

  initializeAuthenticationComponents (decodedToken) {
    this.httpClient.setRequestInterceptor()
    this.httpClient.setResponseInterceptor(AuthenticationEnpoint.RefreshToken)
    this.ability.update(decodedToken.user.rules)
  }

  async login (username, password) {
    try {
      const response = await httpClient.client.post(AuthenticationEnpoint.Token, {
        username: username,
        password: password
      })
      const accessToken = response.data.access
      const decodedToken = jwtDecode(accessToken)
      const token = {
        access: accessToken,
        refresh: response.data.refresh,
        expire: decodedToken.exp
      }
      AuthTokenService.setToken(token)
      this.initializeAuthenticationComponents(decodedToken)
      return decodedToken.user
    } catch (error) {
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

  async logout () {
    this.httpClient.clearAuthorizationHeader()
    AuthTokenService.clearToken()
    this.ability.update([])
  }

  async resetPassword (email) {
    await httpClient.client.post(AuthenticationEnpoint.Token, { email: email })
  }

  async resetPasswordConfirm (uid, token, newPassword) {
    const response = await httpClient.client.post(AuthenticationEnpoint.Token, {
      uid: uid,
      token: token,
      newPassword: newPassword
    })
    return response
  }

  async changePassword (password, newPassword) {
    const response = await httpClient.client.post(AuthenticationEnpoint.Token, {
      password: password,
      newPassword: newPassword
    })
    return response
  }

  getAbility () {
    return this.ability
  }
}

const authRepository = new AuthRepository()
export default authRepository
