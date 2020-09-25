<template>
  <div class="forgot-password neo-morph">
    <h1>Passwort zurücksetzen</h1>
    <b-form @submit.prevent="passwordReset">
      <b-alert v-if="passwordResetError" show variant="danger">{{passwordResetError}}</b-alert>
      <div class="floating-label-input-group">
        <input
          id="forgot-password-input"
          class="form-control"
          v-model="form.email"
          type="text"
          required
          autofocus
          tabindex="1"
          placeholder="E-Mail-Adresse"
        />
        <label for="forgot-password-input">E-Mail-Adresse</label>
      </div>
      <b-button type="submit" variant="success" class="w-75">Zurücksetzen</b-button>
    </b-form>
    <router-link :to="{name: 'Login'}">Zurück zum Login</router-link>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'ForgotPassword',
  data () {
    return {
      form: {
        email: ''
      }
    }
  },
  computed: {
    passwordResetError: function () {
      return this.$store.getters['authentication/passwordResetError']
    }
  },
  methods: {
    passwordReset: function () {
      this.$store.dispatch('authentication/resetPassword', {
        email: this.form.email
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
  .forgot-password {
    display: flex;
    flex-flow: column;
    padding: 2rem;
    margin: 2rem;
    a {
      margin-top: 1rem;
    }
  }
</style>
