<template>
  <div class="mb-[1rem]">
    <table class="table-3">
      <tr>
        <td  class="table-3__data">
          Points Off Turnover
        </td>
        <td class="table-3__data">
          <Input2 
            name="off_turnover"
            :value="classification.off_turnover"
            :classificationId="classification.id"
            type="classification"
          />
        </td>
      </tr>
      <tr>
        <td class="table-3__data">
          Fast Break Points
        </td>
        <td class="table-3__data">
          <Input2 
            name="fast_break"
            :value="classification.fast_break"
            :classificationId="classification.id"
            type="classification"
          />
        </td>
      </tr>
      <tr>
        <td class="table-3__data">
          Second Chance Points
        </td>
        <td
          class="table-3__data"
        >
          <Input2 
            name="second_chance"
            :value="classification.second_chance"
            :classificationId="classification.id"
            type="classification"
          />
        </td>
      </tr>
      <tr>
        <td class="table-3__data">Starter Points</td>
        <td class="table-3__data">
          {{ startersPoints }}
        </td>
      </tr>
      <tr>
        <td class="table-3__data">Bench Points</td>
        <td class="table-3__data">
          {{ benchPoints }}
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
  import { computed, inject, ref, watch } from 'vue';
  import Input2 from './Input2.vue';

  export default {
    components: {
    Input2
},
    props: {
      classification: {},
      team: {}
    },
    setup(props) {

      const startersPoints = computed(() => {
        return computePoints(true)
      })

      const benchPoints = computed(() => {
        return computePoints(false)
      })

      const computePoints = (starter) => {
        let points = 0
        const players = props.team.players

        for (const key in players) {
          if (players[key].is_starter == starter) {
            points += (players[key].stats.two_pts_made * 2)
            points += (players[key].stats.three_pts_made * 3)
            points += players[key].stats.ft_made
          }
        }

        return points
      }


      return {
        ...props,
        startersPoints,
        benchPoints
      }
    }
  }
</script>