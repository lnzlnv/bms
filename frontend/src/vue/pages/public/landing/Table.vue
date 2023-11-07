<template>
  <div>
    <teleport to='#highlights' >
      <HighlightSlider />
    </teleport>
    
    <div class="bg-skew-5 hidden md:block"></div>

    <div class="flex items-center justify-between gap-[10px]">
      <h2 class="hero__standings-title bg-skew-2 w-max mb-[1rem]">
        Season {{ previousSeason.year }}
      </h2>
      
      <select 
        v-model="division"
        class="input-field-8 filter mb-[1rem]"
        name="division" 
        id="division"
      >
        <option value="J">Junior</option>
        <option value="S">Senior</option>
      </select>
    </div>
    
    <table class="table-5">
      <thead>
        <th class="table-5__header">Rank</th>
        <th class="table-5__header">Team</th>
        <th class="table-5__header">Name</th>
        <th class="table-5__header">Wins</th>
      </thead>
      <tbody>
          <tr
            v-for="team, index in teams"
            :key="team.index"
          >
            <td class="table-5__data">
              {{ index + 1 }}
            </td>
            <td class="table-5__data">
              <img 
                class="img-11 mx-[auto]"
                :src="team.team.logo" 
                alt=""
              >
            </td>
            <td class="table-5__data">
              {{ team.team.name }}
            </td>
            <td class="table-5__data">
              {{ team.win }}
            </td>
          </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
  import { computed, onBeforeMount, reactive, ref } from 'vue';
  import axios from 'axios'
  import slider1 from '@composables/slider-1.js';
  import HighlightSlider from './HighlightSlider.vue';

  export default {
    components: {
      HighlightSlider
    },
    setup() {
      const previousSeason = reactive({
        year: '',
        id: ''
      })
      const division = ref('J')
      const allTeams = ref([])
      

      onBeforeMount(() => {
        slider1()
        
        const season = document.getElementById('js-previous-season')
        previousSeason.year = season.dataset.year
        previousSeason.id = season.dataset.id

        const url = '/api/public/standings/all/'
            + previousSeason.id
            + '/'

          axios
            .get(url)
            .then(response => {
              allTeams.value = response.data
            })
      })

      const teams = computed(() => {
        return allTeams.value.filter(team => 
          team.team.division == division.value
        )
      })

      return {
        previousSeason,
        division,
        teams
      }
    }
  }
</script>