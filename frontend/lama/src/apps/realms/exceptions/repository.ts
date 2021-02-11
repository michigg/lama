export class RealmRepositoryException extends Error {
  constructor (message: string) {
    super(message)
    this.name = 'RealmException'
  }
}
