<template>
  <div class='mt-3 col-12 col-md-6'>
  <div class='mb-5'  v-if="grant.metadata">
    <img class='grant-image' :src='grant.metadata.image' height='200px'>
    <h1 class='mt-3'>{{ grant.metadata.name }} - #{{ grant._id }}</h1>
    <p class='grant-owner'><i class="fab fa-ethereum"></i> Created by <a :href='`https://etherscan.io/address/${grant.owner}`' target='_blank'>{{ grant.owner }}</a></p>
    <p class='grant-owner'>
       <i class="fab fa-twitter mr-2"></i> <a :href='`https://twitter.com/${grant.metadata.properties.twitterHandle}`' target='_blank'>
       {{ grant.metadata.properties.twitterHandle }}
    </a></p>
    <p class='grant-owner'>
       <i class="fab fa-github mr-2"></i> <a :href='grant.metadata.properties.projectGithub' target='_blank'>
       {{ grant.metadata.properties.projectGithub }}
    </a></p>
    <h4 id='description' class='subtitle mt-3'>Description</h4>
    <p class='grant-description mt-3'>{{ grant.metadata.description}}</p>
    <h4 id='categories' class='subtitle mt-3'>Categories</h4>
    <div class='mt-3'>
      <button class="btn rounded-pill flex-shrink-0 btn-gc-grey mr-2" :key='category' v-for='category in grant.metadata.properties.keywords'>{{category}}</button>
    </div>
    <h4 class='subtitle mt-3'>Team members</h4>
    <div class='mt-3 extra-bottom'>
	<a target='_blank' :href="`https://gitcoin.co/${handle}`" class='mr-2' :key='handle' v-for='handle in grant.metadata.properties.projectMembers'>
           <img class='mr-2' width=50 height=50  style='border-radius: 50%;' :src='`https://gitcoin.co/dynamic/avatar/${handle}`'>
        {{ handle }}
        </a>
    </div>
    <Quiz :key='grant._id' :grandId='grant._id' @answered='sendCuration' />
  </div>
  </div>
</template>


<script>
import Quiz from './Quiz.vue'

export default {
  name: 'Grant',
  props: [ 'address'],
  components: {Quiz},
  data() {
    return  { 
      grant: {}
    }
  },
  methods: {
    sendCuration(answers) {
    const payload = {
      address: this.address,
      answers: answers,
      grant: this.grant._id
    }
    const host = window.location.hostname
    const port = 5000
  
    fetch(`${window.location.protocol}//${host}:${port}/grant?address=${this.address}`, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow', // manual, *follow, error
      body: JSON.stringify(payload)
    }).then(response => response.json()).then(data => {
        console.log(data)
        alert('Curation completed, yoou has earned 0.1 GTC')
        this.updateGrant()
    })
    },
    updateGrant() {

    const host = window.location.hostname
    const port = 5000
    fetch(`${window.location.protocol}//${host}:${port}/grant?address=${this.address}`, {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow', // manual, *follow, error
    }).then(response => response.json()).then(data => {
        console.log(data)
        this.grant = data 
    })
    }
  },
  mounted(){
    this.updateGrant()
  }
}
</script>

<style>
.grant-image {
    width: 100%;
    object-fit: cover;
    min-height: 250px;
    min-height: max(9vh, 190px);
}

.grant-description {
  color: #333;
}

.extra-bottom {
  margin-bottom: 10rem !important;
}
</style>
