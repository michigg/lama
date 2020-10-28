import axios from 'axios'
import jwtDecode from 'jwt-decode'
import AxiosExtraUtils from '../services/axios'
import AuthTokenService from '../clients/tokenClient'
import { ability } from '../store'
import { AuthenticationEnpoint } from '../api/lama'
import { AuthReposioryException } from '../exceptions/repository'

export default {
  async isLoggedIn () {
    return !!AuthTokenService.getAccessToken()
  },
  async fetchLocalUser () {
    const token = AuthTokenService.getAccessToken()
    if (token) {
      const decodedToken = jwtDecode(token)
      this.initializeAuthenticationComponents(decodedToken)
      return decodedToken.user
    } else {
      return {}
    }
  },
  initializeAuthenticationComponents: function (decodedToken) {
    AxiosExtraUtils.setRequestInterceptor()
    AxiosExtraUtils.setResponseInterceptor(AuthenticationEnpoint.RefreshToken)
    ability.update(decodedToken.user.rules)
  },
  async login (username, password) {
    try {
      const response = await axios.post(AuthenticationEnpoint.Token, {
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
  },
  async logout () {
    delete axios.headers.common.Authorization
    AuthTokenService.clearToken()
    ability.update([])
  },
  async resetPassword (email) {
    await axios.post(AuthenticationEnpoint.Token, { email: email })
  },
  async resetPasswordConfirm (uid, token, newPassword) {
    const response = await axios.post(AuthenticationEnpoint.Token, {
      uid: uid,
      token: token,
      newPassword: newPassword
    })
    return response
  },
  async changePassword (password, newPassword) {
    const response = await axios.post(AuthenticationEnpoint.Token, {
      password: password,
      newPassword: newPassword
    })
    return response
  }
}
