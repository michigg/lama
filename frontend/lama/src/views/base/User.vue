<template>
  <div class="content">
    <router-view/>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'UserBasePage'
}
</script>
<style scoped>
  .content {
    margin-top: var(--nav-height);
  }
</style>
