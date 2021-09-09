<template>
  <nav class="navbar navbar-expand-md navbar-light p-0 px-md-1 w-100">
    <div class='container'>
      <img class="mw-100 logo-static m-2" src="https://s.gitcoin.co/static/v2/images/top-bar/grants-neg.068221dd4d2c.svg" alt="Grants" height="35">
      <span v-if='address'>{{address.slice(0, 10)}}...{{address.slice(-10)}}</span>
      <button class='m-2'  v-on:click='connectWallet' v-else>Connect wallet</button>
    </div>
  </nav>
</template>

<script>
const Web3 = require('web3');

export default {
  name: 'Header',
  data() {
    return {
      address: ''
    }
  },
  mounted() {
    this.connectWallet()
  },
  methods: {
    isMetaMaskInstalled() {
      if (typeof window.ethereum !== 'undefined')  {
         return Boolean(window.ethereum.isMetaMask);
      }
      return false
    },
    async connectWallet() {
      if (this.isMetaMaskInstalled()) { 
         let accounts
         try {
           await window.ethereum.enable();
           const web3 = new Web3(window.ethereum);
           accounts = await web3.eth.getAccounts();

         } catch(e) {
            accounts = await window.ethereum.request({ method: 'eth_accounts' })
         }
         this.address =  accounts[0] || ''
         this.$emit('wallet-connected', this.address)
      }
    }
  }
}
</script>

<style>
nav {
  background-color: black;
  color: #fff;
}

button {
    background-color: #000;
    border: 1px solid #FFF;
}

button:hover {
    background-color: #FFF;
    border: 1px solid #FFF;
    color: #000;
}
</style>
