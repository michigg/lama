<template>
  <div class="content">
    <router-view-transistion />
  </div>
</template>

<script>
// @ is an alias to /src

import RouterViewTransistion from '@/views/base/RouterViewTransistion'

export default {
  name: 'UserBasePage',
  components: { RouterViewTransistion }
}
</script>
<style scoped>
  .content {
    margin-top: var(--nav-height);
    display: flex;
    justify-content: center;
  }
</style>
