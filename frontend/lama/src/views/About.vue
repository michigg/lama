<template>
  <b-container fluid>
    <b-row align-h="center">
      <b-col
        cols="12"
        sm="8"
        md="7"
        lg="6"
        xl="5"
        class="neo-morph text-center p-3 mt-5"
      >
        <p>
          Diese App wurde mit viel <b-icon-heart-fill
            animation="throb"
            variant="danger"
          /> von Michael Götz entwickelt.
        </p>
        <a
          class="nav-item nav-link"
          href="https://github.com/michigg/lama"
          target="_blank"
          rel="noopener noreferrer"
        >Fork me </a>
        <br>
        <h2>Icons</h2>
        Das App-Icon wurde von Freepik von <a href="https://www.flaticon.com">www.flaticon.com</a> erstellt.
        <p>Alle anderen Icons stammen von <a href="https://fontawesome.com"> www.fontawesome.com</a></p>
      </b-col>
    </b-row>
    <b-row align-h="center">
      <b-col
        sm="12"
        md="5"
        class="neo-morph text-center p-3 mx-2 mt-5"
      >
        <h2>Frontend</h2>
        <b-list-group class="text-left">
          <b-list-group-item>
            <span class="font-weight-bold">Paket Version</span><span class="float-right font-weight-bold">Lizenz</span>
          </b-list-group-item>
          <b-list-group-item
            v-for="item in frontendPackages"
            :key="item.package"
            :href="item.link"
            target="_blank"
          >
            {{ item.package }} {{ item.version }} <span class="float-right">{{ item.license }}</span>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col
        sm="12"
        md="5"
        class="neo-morph text-center p-3 mx-2 mt-5"
      >
        <h2>Backend</h2>
        <b-list-group class="text-left">
          <b-list-group-item>
            <span class="font-weight-bold">Paket Version</span><span class="float-right font-weight-bold">Lizenz</span>
          </b-list-group-item>
          <b-list-group-item
            v-for="item in backendPackages"
            :key="item.package"
            :href="item.link"
            target="_blank"
          >
            {{ item.package }} {{ item.version }} <span class="float-right">{{ item.license }}</span>
          </b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>
    <b-row align-h="center">
      <b-col
        cols="12"
        sm="8"
        md="7"
        lg="6"
        xl="5"
        class="text-center p-3 mt-5"
      >
        <router-link :to="{name: 'Home'}">
          Zurück zur Startseite
        </router-link>
      </b-col>
    </b-row>
  </b-container>
</template>
<script lang="ts">
// @ is an alias to /src

import { defineComponent } from 'vue'

export default defineComponent({
  name: 'About',
  data () {
    return {
      frontendPackages: [
        { package: 'Bootstrap', version: '4.4.1', link: '#', license: 'MIT' },
        { package: 'Bootstrap Vue', version: '2.12.0', link: '#', license: 'MIT' },
        { package: 'casl/ability', version: '4.0.7', link: '#', license: 'MIT' },
        { package: 'casl/vue', version: '1.0.3', link: 'https://github.com/stalniy/casl/tree/master/packages/casl-vue', license: 'MIT' },
        { package: 'jwt-decode', version: '2.2.0', link: 'https://github.com/auth0/jwt-decode', license: 'MIT' },
        { package: 'vue-axios', version: '2.1.5', link: 'https://github.com/imcvampire/vue-axios', license: 'MIT' },
        { package: 'axios', version: '0.19.2', link: 'https://github.com/axios/axios', license: 'MIT' },
        { package: 'Vue', version: '2.0.11', link: 'https://github.com/vuejs/vue', license: 'MIT' },
        { package: 'Vuex', version: '3.1.2', link: 'https://github.com/vuejs/vuex', license: 'MIT' }
      ],
      backendPackages: [
        { package: 'Django', version: '3.0.3', link: 'https://github.com/django/django', license: 'BSD 3-Clause' },
        { package: 'django-auth-ldap', version: '2.1.0', link: 'https://github.com/django-auth-ldap/django-auth-ldap', license: 'BSD 2-Clause' },
        { package: 'django-ldapdb', version: '1.4.0', link: 'https://github.com/django-ldapdb/django-ldapdb', license: 'BSD 2-Clause' },
        { package: 'Django Rest Framework', version: '3.11.0', link: 'https://github.com/encode/django-rest-framework', license: 'BSD' },
        { package: 'Simple JWT', version: '4.4.0', link: 'https://github.com/SimpleJWT/django-rest-framework-simplejwt', license: 'MIT' },
        { package: 'Django CORS Headers', version: '3.2.1', link: 'https://github.com/adamchainz/django-cors-headers', license: 'MIT' },
        { package: 'drf-yasg', version: '1.17.1', link: 'https://github.com/axnsan12/drf-yasg', license: 'BSD 3-Clause' }
      ]
    }
  }
})
</script>
