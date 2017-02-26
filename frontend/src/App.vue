<template>
  <div id="vue-app">
    <hello></hello>
  </div>
</template>

<script>
import Hello from './components/Hello.vue'
import PieChart from './components/PieChart.vue'

export default {
  name: 'app',
  components: {
    Hello,
    PieChart
  }
}
</script>
