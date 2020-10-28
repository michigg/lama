// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })
Cypress.Commands.add('getBySel', (selector, ...args) => {
  return cy.get(`[data-test=${selector}]`, ...args)
})
Cypress.Commands.add('vuex', () =>
  cy.window().its('app.$store')
)

Cypress.Commands.add('vuex', () => {
  cy.window().should('have.property', '__store__')
  return cy.window().its('__store__')
})

Cypress.Commands.add('login', (username, password, rememberUser = false) => {
  cy.visit('/')
  cy.vuex().invoke('dispatch', 'authentication/login', {
    username: username,
    password: password
  })
})
