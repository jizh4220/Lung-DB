<template>
  <div class="dashboard-container">
    <div class="dashboard-text"> <center>single-cell RNA-seq Lung DB hosted by Li Lab</center> {{ name }}</div>
    <div class="dashboard-description"> <center>
      There are {{ sample_num }} #sample_num samples, {{ experiment_num }} #experiment_num experiments, 
      {{ disease_num }} #disease_num diseases, {{ tissue_num }} #tissue_num tissue-type, collect by 
      single-cell RNA-seq Lung DB
      </center> </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ]),
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    // margin: 150px;
    line-height: 46px;
  }
}
</style>
