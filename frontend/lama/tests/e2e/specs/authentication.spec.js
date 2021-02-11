// https://docs.cypress.io/api/introduction/api.html
const errorMsg = 'Fehlerhafter Nutzername oder fehlerhaftes Passwort'
const correctCredentials = {
  username: 'michigg',
  password: '2malDrei'
}
const incorrectUsername = {
  username: 'testNutzer',
  password: '2malDrei',
  error: errorMsg
}
const incorrectPassword = {
  username: 'michigg',
  password: 'abcdefgh',
  error: errorMsg
}

const incorrectUsernameAndPassword = {
  username: 'testNutzer',
  password: 'abcdefgh',
  error: errorMsg
}

describe('Login Flow Test', () => {
  beforeEach(() => {
    cy.visit('/login')
    cy.server()
    cy.route('POST', '/api/auth/token/').as('retrieve-token')
  })
  it('wrong user name', () => {
    cy.getBySel('signin-username').type(incorrectUsername.username).find('input').blur()
    cy.getBySel('signin-password').type(incorrectUsername.password).find('input').blur()
    cy.getBySel('signin-submit').click()
    cy.getBySel('signin-error').contains(incorrectUsername.error)
    cy.screenshot('signin-wrong-user-name')
  })
  it('wrong password', () => {
    cy.getBySel('signin-username').type(incorrectPassword.username).find('input').blur()
    cy.getBySel('signin-password').type(incorrectPassword.password).find('input').blur()
    cy.getBySel('signin-submit').click()
    cy.getBySel('signin-error').contains(incorrectPassword.error)
    cy.screenshot('signin-wrong-password')
  })
  it('wrong user name and password', () => {
    cy.getBySel('signin-username').type(incorrectUsernameAndPassword.username).find('input').blur()
    cy.getBySel('signin-password').type(incorrectUsernameAndPassword.password).find('input').blur()
    cy.getBySel('signin-submit').click()
    cy.getBySel('signin-error').contains(incorrectUsernameAndPassword.error)
    cy.screenshot('signin-wrong-user-name-user-name')
  })
  it('correct login', () => {
    cy.getBySel('signin-username').type(correctCredentials.username).find('input').blur()
    cy.getBySel('signin-password').type(correctCredentials.password).find('input').blur()
    cy.getBySel('signin-submit').click()
    cy.location('pathname').should('equal', '/realm')
  })
  it('link to forgot password', () => {
    cy.getBySel('forgot-password-link').click()
    cy.location('pathname').should('equal', '/forgot-password')
  })
  it('should redirect unauthenticated user to signin page', () => {
    cy.visit('/realm')
    cy.location('pathname').should('equal', '/login')
  })
})
