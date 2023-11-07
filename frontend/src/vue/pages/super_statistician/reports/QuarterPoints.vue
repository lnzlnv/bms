<template>
  <div>
    <table class="table-3">
      <thead>
        <tr>
          <th>Total Points</th>
          <th>{{ totalPoints }}</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="point in points"
          :key="point.id"
          class="quarters"
        >
          <td class="table-3__data">
            <span class="quarter-name">{{ point.quarter }}</span> Quarter
          </td>
          <td class="table-3__data">
            <Input2 
              name="points"
              :value="point.points"
              :classificationId="point.id"
              type="quarter"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import Input2 from './Input2.vue';

  export default {
    components: {
    Input2
},
    props: {
      points: {},
      totalPoints: Number
    },
    setup(props) {
      return{
        ...props
      }
    }
  }
</script>