// TODO: automatic set enpoint
const BaseUrl = 'http://localhost:8888/api/v1'
export const UserEndpoint = {
  User: (realmId: number, userDn: string) => `${BaseUrl}/realm/${realmId}/user/${userDn}/`,
  Users: (realmId: number) => `${BaseUrl}/realm/${realmId}/user/`
}
