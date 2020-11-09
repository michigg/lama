<template>
  <div class="login neo-morph">
    <h1>Login</h1>
    <b-form @submit.prevent="login">
      <b-alert
        v-if="loginError"
        show
        variant="danger"
      >
        {{ loginError }}
      </b-alert>
      <div class="floating-label-input-group">
        <input
          id="login-username-input"
          v-model="form.username"
          class="form-control"
          type="text"
          required
          autofocus
          tabindex="1"
          placeholder="Benutzername"
        >
        <label for="login-username-input">Benutzername</label>
      </div>
      <div class="floating-label-input-group">
        <input
          id="login-password-input"
          v-model="form.password"
          class="form-control"
          type="password"
          required
          autofocus
          tabindex="2"
          placeholder="Passwort"
        >
        <label for="login-password-input">Passwort</label>
      </div>
      <b-button
        type="submit"
        variant="success"
        class="w-75"
      >
        Anmelden
      </b-button>
    </b-form>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'ForgotPasswordConfirm',
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  computed: {
    loginError: function () {
      return this.$store.getters['authentication/loginError']
    }
  },
  methods: {
    login: function () {
      this.$store.dispatch('authentication/login', {
        username: this.form.username,
        password: this.form.password
      })
        .then(() => {
          // if (this.$route.query.redirect) {
          //   this.$router.push(this.$route.query.redirect)
          // } else {
          //   this.$router.push('/')
          // }
        })
        .catch()
    }
  }
}
</script>
<style lang="scss" scoped>
  .login {
    display: flex;
    flex-flow: column;
    padding: 2rem;
    margin: 2rem;
  }
</style>
