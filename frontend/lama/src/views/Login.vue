<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" sm=12 md="5" class="mt-3 p-4 shadow bg-dark">
        <b-form @submit.prevent="login">
          <b-form-group>
            <b-form-input
              v-model="username"
              type="text"
              required
              placeholder="Username"
            ></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input
              v-model="password"
              type="password"
              required
              placeholder="Passwort"
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary" class="w-75 rounded-0">Anmelden</b-button>
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
      username: '',
      password: ''
    }
  },
  methods: {
    login: function () {
      this.$store.dispatch('authentication/login', {
        username: this.username,
        password: this.password
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
