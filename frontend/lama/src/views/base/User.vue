<template>
  <div class="content">
    <router-view-transistion />
  </div>
</template>

<script lang="ts">
// @ is an alias to /src

import RouterViewTransistion from '@/views/base/RouterViewTransistion.vue'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UserBasePage',
  components: { RouterViewTransistion }
})
</script>
<style scoped>
  .content {
    margin-top: var(--nav-height);
    display: flex;
    justify-content: center;
  }
</style>
