<template>
  <div>
    <Table 
        :team="team"
      />
    <div class="md:grid grid-2-column-2 gap-[20px] lg:flex lg:justify-center lg:gap-[100px]">
      <PointsClassification 
        :classification="team.points_classification"
        :team="team"
      />
      <QuarterPoints 
        :points="team.points_per_quarter"
        :totalPoints="totalPoints"
      />
    </div>
  </div>
</template>

<script>
  import Table from './Table.vue';
  import PointsClassification from './PointsClassification.vue';
  import QuarterPoints from './QuarterPoints.vue';


  export default {
    components: {
      Table,
      PointsClassification,
      QuarterPoints
    },
    props: {
      team: {},
      totalPoints: Number
    },
    setup(props) {
      return {
        ...props
      }
    }
  }
</script>

<style lang="scss" scoped>

</style>