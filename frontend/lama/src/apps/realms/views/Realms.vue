<template>
  <b-container>
    <headline title="Bereiche" />
    {{ error }} Hello World
    <loading-info v-if="loading" />
    <b-alert
      v-else-if="error"
      show
      variant="danger"
    >
      {{ error }}
    </b-alert>
    <realms-table v-else-if="rows" />
    <b-alert
      v-else
      variant="info"
      show=""
      data-test="realms-empty-result-info"
    >
      Ihrem Account scheinen noch keine Bereiche zur Administration freigegeben worden sein.
    </b-alert>
  </b-container>
</template>

<script>
// @ is an alias to /src
import Headline from '@/components/utils/Headline'
import RealmsTable from '@/apps/realms/components/RealmsTable'
import LoadingInfo from '@/components/utils/LoadingInfo'

export default {
  name: 'Realms',
  components: {
    LoadingInfo,
    RealmsTable,
    Headline
  },
  computed: {
    rows () {
      return this.$store.getters['realms/realms'].length
    },
    loading () {
      return this.$store.getters['realms/loading']
    },
    error () {
      return this.$store.getters['realms/loading']
    }
  },
  mounted () {
    this.$store.dispatch('realms/fetchRealms')
  }
}
</script>

<style scoped>
.floating-label-input-group {
  display: -webkit-box !important;
  display: -ms-flexbox !important;
  display: flex !important;
}

.floating-label-input-group > .form-control {
  min-width: 0;
}
</style>
