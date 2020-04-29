<template>
  <b-container fluid>
    <b-row align-h="center">
      <b-col cols="12" sm="8" md="7" lg="6" xl="5" class="shadow text-center p-3 mt-5">
        <p>Diese App wurde mit viel von Michael Götz entwickelt.</p>
        <a class="nav-item nav-link" href="https://github.com/michigg/lama" target="_blank">Fork me </a>
        <br>
        <h2>Icons</h2>
        Das App-Icon wurde von Freepik von <a href="https://www.flaticon.com">www.flaticon.com</a> erstellt.
        <p>Alle anderen Icons stammen von <a href="https://fontawesome.com"> www.fontawesome.com</a></p>
      </b-col>
    </b-row>
    <b-row align-h="center">
      <b-col sm="12" md="5" class="shadow text-center p-3 mx-1 mt-5">
        <h2>Frontend</h2>
        <b-list-group class="text-left">
          <b-list-group-item>
            Paket Version <span class="float-right">Lizenz</span>
          </b-list-group-item>
          <b-list-group-item v-for="item in frontendPackages" :key="item.package" :href="item.link">
            {{item.package}} {{item.version}} <span class="float-right">{{item.license}}</span>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col sm="12" md="5" class="shadow text-center p-3 mx-1 mt-5">
        <h2>Backend</h2>
         <b-list-group class="text-left">
           <b-list-group-item>
              Paket Version <span class="float-right">Lizenz</span>
            </b-list-group-item>
            <b-list-group-item v-for="item in backendPackages" :key="item.package" :href="item.link">
              {{item.package}} {{item.version}} <span class="float-right">{{item.license}}</span>
            </b-list-group-item>
         </b-list-group>
      </b-col>
    </b-row>
    <b-row align-h="center">
      <b-col cols="12" sm="8" md="7" lg="6" xl="5" class="text-center p-3 mt-5">
        <router-link :to="{name: 'Home'}">Zurück zur Startseite</router-link>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
// @ is an alias to /src

export default {
  name: 'About',
  data () {
    return {
      frontendPackages: [
        { package: 'Bootstrap', version: '4', link: '#', license: 'TEST' },
        { package: 'Vue Bootstrap', version: '4', link: '#', license: 'TEST' },
        { package: 'CASL', version: '4', link: '#', license: 'TEST' },
        { package: 'Vue', version: '4', link: '#', license: 'TEST' },
        { package: 'Vuex', version: '4', link: '#', license: 'TEST' }
      ],
      backendPackages: [
        { package: 'Django', version: '4', link: '#', license: 'TEST' },
        { package: 'django-auth-ldap', version: '4', link: '#', license: 'TEST' },
        { package: 'django-ldapdb', version: '4', link: '#', license: 'TEST' },
        { package: 'Django Rest Framework', version: '4', link: '#', license: 'TEST' },
        { package: 'Simple JWT', version: '4', link: '#', license: 'TEST' },
        { package: 'Django CORS Headers', version: '4', link: '#', license: 'TEST' },
        { package: 'drf-yasg', version: '4', link: '#', license: 'TEST' }
      ]
    }
  }
}
</script>
