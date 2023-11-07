<template>
  <div>
    <div v-if="!game.full_time_analysis_can_be_generated">
      <h1 class="title-3">Full-Time Analysis will be generated after the game ended.</h1>
    </div>

    <Analysis 
      v-if="game.has_full_time_analysis"
      :homeStats="game.home_team.full_time_analysis.stats"
      :awayStats="game.away_team.full_time_analysis.stats"
      :homePointsClassification="game.home_team.full_time_analysis.points_classification"
      :awayPointsClassification="game.away_team.full_time_analysis.points_classification"
      name="Full-Time Analysis"
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
        ...props,
      }
    }
  }
</script>