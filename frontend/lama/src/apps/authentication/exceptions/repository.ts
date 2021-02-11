export class AuthRepositoryException extends Error {
  constructor (message: string) {
    super(message)
    this.name = 'ValidationError'
  }
}
