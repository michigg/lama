// TODO: automatic set enpoint
const BaseUrl = 'http://localhost:8888/api/v1'.concat('/realm')
export const RealmEndpoint = {
  Realm: (id: number) => BaseUrl + '/' + id + '/',
  Realms: BaseUrl + '/'
}
