import { Ability } from '@casl/ability'

export class User {
  public username: string
  public email: string
  public ability: Ability
  public sessionExpirationTime: Date

  constructor (username: string, email: string, ability: Ability, sessionExpirationTime: Date) {
    this.username = username
    this.email = email
    this.ability = ability
    this.sessionExpirationTime = sessionExpirationTime
  }

  isEmpty () {
    return !this.username
  }

  static emptyUser () {
    return new User('', '', new Ability([]), new Date())
  }
}
