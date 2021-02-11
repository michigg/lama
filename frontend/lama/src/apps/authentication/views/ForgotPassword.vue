<template>
  <div class="forgot-password neo-morph">
    <h1>Passwort zurücksetzen</h1>
    <b-form @submit.prevent="passwordReset">
      <b-alert
        :show="passwordResetError"
        variant="danger"
      >
        {{ passwordResetError }}
      </b-alert>
      <div class="floating-label-input-group">
        <input
          id="forgot-password-input"
          v-model="form.email"
          class="form-control"
          type="text"
          required
          autofocus
          tabindex="1"
          placeholder="E-Mail-Adresse"
        >
        <label for="forgot-password-input">E-Mail-Adresse</label>
      </div>
      <b-button
        type="submit"
        variant="success"
        class="w-75"
      >
        Zurücksetzen
      </b-button>
    </b-form>
    <router-link :to="{name: 'Login'}">
      Zurück zum Login
    </router-link>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src

import { useStore } from '@/store'
import { defineComponent } from 'vue'

export default defineComponent({
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
      const store = useStore()
      return store.getters['authentication/passwordResetError']
    }
  },
  methods: {
    passwordReset: function () {
      const store = useStore()
      store.dispatch('authentication/resetPassword', {
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
})
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
