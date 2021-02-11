// https://docs.cypress.io/api/introduction/api.html

describe('Add Realm Test', () => {
  beforeEach(() => {
    cy.login('michigg', '2malDrei')
    cy.visit('/realm-add')
  })
  it('elements exists', () => {
  })
  it('correct input', () => {
  })
  it('feedback on wrong dn', () => {
  })
  it('feedback missing name', () => {
  })
  it('redirect to realm detail on success', () => {
  })
  it('redirect to realms on abort', () => {
  })
})
