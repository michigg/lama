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
