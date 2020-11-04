<template>
  <div class="home">
    <admin-sidebar />
    <div class="content">
      <router-view-transistion />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import AdminSidebar from '../../components/utils/AdminSidebar'
import RouterViewTransistion from '@/views/base/RouterViewTransistion'

export default {
  name: 'AdminBasePage',
  components: {
    RouterViewTransistion,
    AdminSidebar
  },
  computed: {
    isLoggedIn: function () {
      return this.$store.getters['authentication/isLoggedIn']
    }
  }
}
</script>

<style scoped>
  @media (max-width: 767px) {
    .content {
      margin-top: var(--nav-height) + 1rem;
    }
  }

  @media (min-width: 768px) {
    .content {
      margin-top: calc(var(--nav-height) + 1rem);
      margin-left: var(--admin-bar-width);
    }
  }
</style>
