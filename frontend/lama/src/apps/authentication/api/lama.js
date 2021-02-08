const BaseUrl = 'http://localhost:8000/api'.concat('/auth')

export const AuthenticationEndpoint = {
  Token: BaseUrl + '/token/',
  RefreshToken: BaseUrl + '/token/refresh/'
}
