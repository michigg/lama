class Group {}

export class User {
  public dn: string
  public name: string
  public displayName: string
  public email: string
  public groups: Array<Group>
  public lastLogin: Date

  constructor (
    dn: string,
    name: string,
    displayName: string,
    email: string,
    groups: Array<Group>,
    lastLogin: Date) {
    this.dn = dn
    this.name = name
    this.displayName = displayName
    this.email = email
    this.groups = groups
    this.lastLogin = lastLogin
  }

  static emptyUser () {
    return new User('', '', '', '', [], new Date())
  }
}
