export class UserRepositoryException extends Error {
  constructor (message: string) {
    super(message)
    this.name = 'UserException'
  }
}
