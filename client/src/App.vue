<template>
  <div id="app">
    <Header @wallet-connected='updateAddress' />
    <Grant :address="address"/>
  </div>
</template>

<script>
import Grant from './components/Grant.vue'
import Header from './components/Header.vue'
export default {
  name: 'App',
  components: {
    Grant,
    Header
  },
  data() {
    return {
      address: ''
    }
  },
  methods: {
    updateAddress(value) {
      this.address = value
    }
  }
}
</script>

<style>
#app {  
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
