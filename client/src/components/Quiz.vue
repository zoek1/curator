<template>
  <div class='quiz'>
     <p class='question'>{{ questions[step].text }}</p>
     <button class='btn btn-lg btn-danger font-weight-semibold mr-3' v-on:click='setNoAnswer'>No</button>
     <button class='btn btn-lg btn-warning  mr-3' v-on:click='setUnsureAnswer'>Unsure</button>
     <button class='btn btn-lg btn-success font-weight-semibold' v-on:click='setYesAnswer'>Yes</button>
  </div>
</template>

<script>
export default {
  name: 'Quiz',
  props: ['grantId'],
  data() {
     return {
       questions: [
         {id: 'coming_from_a_legitimate_project', text: 'This grant comes from a legitimate project?'},
         {id: 'having_a_reasonable_description', text: 'This grant has a reasonable description?', ref: 'description'},
         {id: 'not_being_offensive', text: 'This grant isn\'t offensive?'},
         {id: 'correct_category', text: 'This grant being in the correct category?', ref: 'categories'},
         {id: 'category_is_allowed_on_the_platform', text: 'This grant being in a category that is allowed on the platform?'},
       ],
     step: 0
     }
  },
  methods: {
    setYesAnswer() { this.setAnswer('yes') },
    setNoAnswer() { this.setAnswer('no') },
    setUnsureAnswer() { this.setAnswer('unsure') },
    setAnswer(answer) {
      this.questions[this.step].answer = answer
      this.step = this.step + 1 

      if (this.step >= this.questions.length) {
        this.$emit('answered', this.questions)
      }

      if (this.questions[this.step].ref) {
         document.getElementById(this.questions[this.step].ref).scrollIntoView();
      }

    }
  }
}
</script>

<style>
.quiz {
    position: fixed;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    width: 100%;
    margin: 0;
    left: 0;
    text-align: center;
    padding-top: 15px;
    padding-bottom: 15px;
    color: white;
    font-size: 1.5em;
}
</style>
