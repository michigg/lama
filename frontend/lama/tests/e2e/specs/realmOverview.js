// https://docs.cypress.io/api/introduction/api.html

describe('Realm Overview Test', () => {
  beforeEach(() => {
    cy.login('michigg', '2malDrei')
  })
  it('elements exists', () => {
    cy.visit('realm')
    cy.getBySel('realms-table').should('exist')
    cy.getBySel('realms-table-search-input').should('exist')
    cy.getBySel('realms-table-search-input-clear-button').should('exist')
    cy.getBySel('realms-table-page-count-selector').should('exist')
    cy.getBySel('realms-table-pagination').should('exist')
  })
  it('pagination only shown if page size smaller result size', () => {
  })
  it('search is implemented', () => {
  })
  it('search clear button is implemented', () => {
  })
  it('page size selector is implemented', () => {
  })
  it('empty response', () => {
  })
})
