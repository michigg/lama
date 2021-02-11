export class Realm {
  public id: number
  public name: string
  public email: string
  public ldapBaseDn: string
  public adminGroup: object
  public defaultGroup: object
  public userCount: number
  public groupCount: number

  constructor (
    id: number,
    name: string,
    email: string,
    ldapBaseDn: string,
    adminGroup: object,
    defaultGroup: object,
    userCount: number,
    groupCount: number) {
    this.id = id
    this.name = name
    this.email = email
    this.ldapBaseDn = ldapBaseDn
    this.adminGroup = adminGroup
    this.defaultGroup = defaultGroup
    this.userCount = userCount
    this.groupCount = groupCount
  }

  static emptyRealm () {
    return new Realm(-1, '', '', '', {}, {}, -1, -1)
  }
}
