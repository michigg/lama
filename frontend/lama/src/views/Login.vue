<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" sm=12 md="10" lg="8" xl="5" class="mt-4 p-4 shadow">
        <b-form @submit.prevent="login">
          <div class="floating-label-input-group">
            <input
              id="username-input"
              class="form-control"
              v-model="form.username"
              type="text"
              required
              autofocus
              tabindex="1"
              placeholder="Benutzername"
            />
            <label for="username-input">Benutzername</label>
          </div>
          <div class="floating-label-input-group">
            <input
              id="password-inputs"
              class="form-control"
              v-model="form.password"
              type="password"
              required
              autofocus
              tabindex="2"
              placeholder="Passwort"
            />
            <label for="password-inputs">Passwort</label>
          </div>
          <b-button type="submit" variant="success" class="w-75">Anmelden</b-button>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
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
      }
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
        .catch((error) => console.log(error))
    }
  }
}
</script>
