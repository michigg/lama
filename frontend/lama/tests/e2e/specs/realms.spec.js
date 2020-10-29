// https://docs.cypress.io/api/introduction/api.html

const emptyRealmResponseMessage = 'Ihrem Account scheinen noch keine Bereiche zur Administration freigegeben worden sein.'

describe('Realm Overview Test', () => {
  beforeEach(() => {
    cy.login('michigg', '2malDrei')
    cy.server()
    cy.fixture('realms/realms_3.json').as('realmsSmall')
    cy.route('GET', '/api/v1/realm/', '@realmsSmall')
    cy.visit('/realm')
  })
  it('elements exists', () => {
    cy.visit('realm')
    cy.getBySel('realms-table').should('exist')
    cy.getBySel('realms-table-search-input').should('exist')
    cy.getBySel('realms-table-search-input-clear-button').should('exist')
    cy.getBySel('realms-table-page-count-selector').should('exist')
    cy.getBySel('realms-empty-result-info').should('not.exist')
  })
  it('hide pagination on small realm count', () => {
    cy.getBySel('realms-table-pagination').should('not.exist')
  })
  it('show pagination on large realm counts', () => {
    cy.fixture('realms/realms_26.json').as('realmsLarge')
    cy.route('GET', '/api/v1/realm/', '@realmsLarge')
    cy.visit('/realm')
    cy.getBySel('realms-table-pagination').should('exist')
  })
  it('search is implemented', () => {
  })
  it('search clear button is implemented', () => {
  })
  it('page size selector is implemented', () => {
  })
  it('empty response', () => {
    cy.fixture('realms/realms_empty.json').as('emptyRealms')
    cy.route('GET', '/api/v1/realm/', '@emptyRealms')
    cy.visit('/realm')
    cy.getBySel('realms-table').should('not.exist')
    cy.getBySel('realms-table-search-input').should('not.exist')
    cy.getBySel('realms-table-search-input-clear-button').should('not.exist')
    cy.getBySel('realms-table-page-count-selector').should('not.exist')
    cy.getBySel('realms-empty-result-info')
      .should('exist')
      .contains(emptyRealmResponseMessage)
  })
})
