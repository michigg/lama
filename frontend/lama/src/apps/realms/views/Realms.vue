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

<script lang="ts">
// @ is an alias to /src
import Headline from '@/components/utils/Headline.vue'
import RealmsTable from '@/apps/realms/components/RealmsTable.vue'
import LoadingInfo from '@/components/utils/LoadingInfo.vue'
import { useStore } from '@/store'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Realms',
  components: {
    LoadingInfo,
    RealmsTable,
    Headline
  },
  computed: {
    rows () {
      const store = useStore()
      return store.getters['realms/realms'].length
    },
    loading () {
      const store = useStore()
      return store.getters['realms/loading']
    },
    error () {
      const store = useStore()
      return store.getters['realms/loading']
    }
  },
  mounted () {
    const store = useStore()
    store.dispatch('realms/fetchRealms')
  }
})
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
