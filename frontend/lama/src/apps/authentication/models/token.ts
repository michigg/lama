import { User } from '@/apps/authentication/models/user'
import { ApiTokenUserInterface } from '@/apps/authentication/interfaces/token'

export class Token {
  public accessToken: string
  public refreshToken: string
  public user: ApiTokenUserInterface | null
  public sessionExpirationTime: Date

  constructor (accessToken: string, refreshToken: string, user: ApiTokenUserInterface | null, expirationTime: Date) {
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
