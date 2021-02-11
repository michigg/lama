<template>
  <div class="home">
    <admin-sidebar />
    <div class="content">
      <router-view-transistion />
    </div>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import AdminSidebar from '../../components/utils/AdminSidebar.vue'
import RouterViewTransistion from '@/views/base/RouterViewTransistion.vue'
import { useStore } from '@/store'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AdminBasePage',
  components: {
    RouterViewTransistion,
    AdminSidebar
  },
  computed: {
    isLoggedIn: function () {
      const store = useStore()
      return store.getters['authentication/isLoggedIn']
    }
  }
})
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
