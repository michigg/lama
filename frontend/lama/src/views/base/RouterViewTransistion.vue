<template>
  <transition :name="transitionName">
    <router-view class="child-view" />
  </transition>
</template>
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RouterViewTransistion',
  data () {
    return {
      transitionName: 'slide-left'
    }
  },
  watch: {
    '$route' (to, from) {
      const toDepth = to.path.split('/').length
      const fromDepth = from.path.split('/').length
      this.transitionName = toDepth < fromDepth ? 'slide-left' : 'slide-right'
    }
  }
})
</script>
<style>
/*.fade-enter-active, .fade-leave-active {*/
/*  transition: opacity .75s ease;*/
/*}*/

/*.fade-enter, .fade-leave-active {*/
/*  opacity: 0;*/
/*}*/

/*.child-view {*/
/*  position: absolute;*/
/*  transition: all .75s cubic-bezier(.55, 0, .1, 1);*/
/*}*/

/*.slide-left-enter, .slide-right-leave-active {*/
/*  opacity: 0;*/
/*  -webkit-transform: translate(50%, 0);*/
/*  transform: translate(250%, 0);*/
/*}*/

/*.slide-left-leave-active, .slide-right-enter {*/
/*  opacity: 0;*/
/*  -webkit-transform: translate(-50%, 0);*/
/*  transform: translate(-250%, 0);*/
/*}*/
</style>
