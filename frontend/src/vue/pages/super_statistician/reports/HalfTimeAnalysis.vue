<template>
  <div>
    <div v-if="!game.has_half_time_analysis">
      <h1 class="title-3">Half-Time Analysis will be generated after the first half.</h1>
    </div>
    
    <Analysis 
      v-if="game.has_half_time_analysis"
      :homeStats="game.home_team.half_time_analysis.stats"
      :awayStats="game.away_team.half_time_analysis.stats"
      :homePointsClassification="game.home_team.half_time_analysis.points_classification"
      :awayPointsClassification="game.away_team.half_time_analysis.points_classification"
      name="Half-Time Analysis"
    />
  </div>
</template>

<script>
  import Analysis from './Analysis.vue'

  export default {
    components: {
      Analysis
    },
    props: {
      game: {}
    },
    setup(props) {
      return {
        ...props
      }
    }
  }
</script>