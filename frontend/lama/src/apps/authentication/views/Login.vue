<template>
  <div class="login neo-morph bg-light">
    <h1>Login</h1>
    <b-form @submit.prevent="login">
      <b-alert
        :show="!!error"
        variant="danger"
        data-test="signin-error"
      >
        {{ error }}
      </b-alert>
      <div
        class="floating-label-input-group"
        data-test="signin-username"
      >
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
      <div
        class="floating-label-input-group"
        data-test="signin-password"
      >
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
        data-test="signin-submit"
      >
        Anmelden
      </b-button>
    </b-form>
    <router-link
      :to="{name: 'ForgotPassword'}"
      class="forgot-password-link"
      data-test="forgot-password-link"
    >
      Passwort vergessen?
    </router-link>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Login',
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      error: '',
      loading: false
    }
  },
  computed: {
    loginError: function () {
      return this.$store.getters['authentication/loginError']
    }
  },
  methods: {
    async login () {
      this.error = ''
      this.loading = true
      try {
        await this.$store.dispatch('authentication/login', {
          username: this.form.username,
          password: this.form.password
        })
        if (this.$route.query.redirect) {
          await this.$router.push({ path: this.$route.query.redirect })
        } else {
          await this.$router.push({ name: 'Home' })
        }
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
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
  transition: all;

  .forgot-password-link {
    margin-top: 1rem;
  }
}
</style>
