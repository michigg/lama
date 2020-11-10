export class Realm {
  constructor (id, name, email, ldapBaseDn, adminGroup, defaultGroup, userCount, groupCount) {
    this.id = id
    this.name = name
    this.ldapBaseDn = ldapBaseDn
    this.adminGroup = adminGroup
    this.defaultGroup = defaultGroup
    this.userCount = userCount
    this.groupCount = groupCount
  }
}
