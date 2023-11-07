<template>
  <div class="container-2 flex justify-evenly mb-[2.875rem]">
      <div 
        v-for="team in teams"
        class="px-[0.5em]"
      >
        <img
          class="img-1 mx-0"
          :src="team.team.logo" 
        >
      </div>
  </div>

  <div class="px-[1em] mb-[2rem] relative lg:px-[5.5em]">
    <div 
      v-if="isLoading"
      class="loading-3 flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div class="md:flex items-center justify-between">
      <div class="mb-[1rem]">
        <button 
          @click="activeTab = 'ELIMINATIONS'"
          :class="activeTab == 'ELIMINATIONS' ? 'active': ''"
          class="btn-21"
        >
          Eliminations
        </button>
        <button 
          @click="activeTab = 'PLAYOFFS'"
          :class="activeTab == 'PLAYOFFS' ? 'active': ''"
          class="btn-21"
        >
          Playoffs
        </button>
      </div>
      <form class="mb-[1rem] flex justify-end items-start gap-[20px]">
        <div class="mb-[1rem] md:mb-0">
          <select
            v-model="season"
            class="input-field-5 w-full"
            name="division"
            id="division"
          >
            <option value="" disabled selected>Select Season</option>
            <option
              v-for="season in options.seasons"
              :key="season.id"
              :value="season.id"
            >
              {{ season.year }}
            </option>
          </select>
        </div>
        <div>
          <select
            v-model="division"
            class="input-field-5 w-full"
            name="division"
            id="division"
          >
            <option value="" disabled selected>Select Division</option>
            <option value="J">Junior</option>
            <option value="S">Senior</option>
          </select>
        </div>
      </form>
    </div>

    <div class="scroll-container overflow-x-auto">
      <table class="table-1 stats">
        <thead>
          <tr>
            <th class="table-1__header">RANK</th>
            <th class="table-1__header">NAME</th>
            <th 
              class="table-1__header" 
              title="Games Played"
            >
              GP
            </th>
            <th 
              class="table-1__header" 
              title="Win"
            >
              W
            </th>
            <th 
              class="table-1__header" 
              title="Lose"
            >
              L
            </th>
            <th 
              class="table-1__header text-right" 
              title="Points Per Game"
            >
              PPG
            </th>
            <th 
              class="table-1__header text-right" 
              title="Field Goals Made"
            >
              FGM
            </th>
            <th 
              class="table-1__header text-right" 
              title="Field Goals Attempt"
            >
              FGA
            </th>
            <th 
              class="table-1__header text-right"
              title="Field Goals Percentage"
            >
              FG%
            </th>
            <th 
              class="table-1__header text-right"
              title="2 Points Made"
            >
              2PM
            </th>
            <th 
              class="table-1__header text-right"
              title="2 Points Attempt"
            >
              2PA
            </th>
            <th 
              class="table-1__header text-right"
              title="3 Points Percentage"
            >
              2P%
            </th>
            <th 
              class="table-1__header text-right"
              title="3 Points Made"
            >
              3PM
            </th>
            <th 
              class="table-1__header text-right"
              title="3 Points Attempt"
            >
              3PA
            </th>
            <th 
              class="table-1__header text-right"
              title="3 Points Percentage"
            >
              3P%
            </th>
            <th 
              class="table-1__header text-right"
              title="Free Throws Made"
            >
              FTM
            </th>
            <th 
              class="table-1__header text-right"
              title="Free Throws Attempt"
            >
              FTA
            </th>
            <th 
              class="table-1__header text-right"
              title="Free Throw Percentage"
            >
              FT%
            </th>
            <th 
              class="table-1__header text-right"
              title="Offensive Rebounds"
            >
              OREB
            </th>
            <th 
              class="table-1__header text-right"
              title="Defensive Rebounds"
            >
              DREB
            </th>
            <th 
              class="table-1__header text-right"
              title="Total Rebounds"
            >
              REB
            </th>
            <th 
              class="table-1__header text-right"
              title="Assists"
            >
              AST
            </th>
            <th 
              class="table-1__header text-right"
              title="Turnovers"
            >
              TO
            </th>
            <th 
              class="table-1__header text-right"
              title="Steals"
            >
              STL
            </th>
            <th 
              class="table-1__header text-right"
              title="Blocks"
            >
              BLK
            </th>
          </tr>
        </thead>
        <tbody
          v-if="teams.length > 0"
        >
          <tr 
            v-for="(team, index) in teams"
            :key="team.id"
            class="table-1__row flex flex-col lg:table-row"
          >
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="RANK"
            >
              {{ index + 1 }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="NAME"
            >
              {{ team.team.name }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="GP"
            >
              {{ team.games_played == 0 ? '-' : team.games_played }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="W"
            >
              {{ team.games_played == 0 ? '-' : team.win }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="L"
            >
              {{ team.games_played == 0 ? '-' : team.lose }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="PTS"
            >
              {{ team.games_played == 0 ? '-' : team.pts_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FGM"
            >
              {{ team.games_played == 0 ? '-' : team.field_goal_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FGA"
            >
              {{ team.games_played == 0 ? '-' : team.field_goals_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FG%"
            >
              {{ team.games_played == 0 ? '-' : team.stat.total_fg_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PM"
            >
              {{ team.games_played == 0 ? '-' : team.two_pts_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PA"
            >
              {{ team.games_played == 0 ? '-' : team.two_pts_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3P%"
            >
              {{ team.games_played == 0 ? '-' : team.stat.two_pts_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PM"
            >
              {{ team.games_played == 0 ? '-' : team.three_pts_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PA"
            >
              {{ team.games_played == 0 ? '-' : team.three_pts_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3P%"
            >
              {{ team.games_played == 0 ? '-' : team.stat.three_pts_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FTM"
            >
              {{ team.games_played == 0 ? '-' : team.ft_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FTA"
            >
              {{ team.games_played == 0 ? '-' : team.ft_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell"
              data-cell="FT%"
            >
              {{ team.games_played == 0 ? '-' : team.stat.ft_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="OREB"
            >
              {{ team.games_played == 0 ? '-' : team.reb_off_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="DREB"
            >
              {{ team.games_played == 0 ? '-' : team.reb_def_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="REB"
            >
              {{ team.games_played == 0 ? '-' : team.reb_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="AST"
            >
              {{ team.games_played == 0 ? '-' : team.assists_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="TO"
            >
              {{ team.games_played == 0 ? '-' : team.turnovers_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="STL"
            >
              {{ team.games_played == 0 ? '-' : team.steals_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px]  lg:table-cell "
              data-cell="STL"
            >
              {{ team.games_played == 0 ? '-' : team.blocks_per_game }}
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr class="table-1__row flex flex-col lg:table-row">
            <td
              class="table-1__data empty text-center grid grid-2-column-3 gap-[10px]  lg:table-cell"
              colspan="25"
            >
              No available stats
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { computed, onBeforeMount, ref, watch } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import success from '@composables/generate-account/success.js'

  export default {
    components: {
      LoadingSpinner
    },
    setup() {
      const allTeams = ref([])
      const season = ref("")
      const division = ref('J')
      const options = ref({})
      const activeTab = ref('ELIMINATIONS')
      const isLoading = ref(false)
      const hasError = success()

      onBeforeMount(() => {
        isLoading.value = true
        const url = '/api/public/players/options/'

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            season.value = response.data.current_season.id
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      /**
       * Watch
       */
        watch(
          [season, activeTab],
          () => {
            isLoading.value = true
            const url = '/api/public/standings/all/'
              + season.value
              + '/'
              + `?standing_type=${activeTab.value}`
            
            axios
              .get(url)
              .then(response => {
                allTeams.value = response.data
                isLoading.value = false
              })
              .catch(err => {
                isLoading.value = false
                hasError.value = true
              })
          }
        )
      /**
       * End of Watch
       */

      /**
       * Computed
       */
        const teams = computed(() => {
          return allTeams.value.filter(team => 
            team.team.division == division.value
          )
        })
      /**
       * Computed
       */

      return {
        season,
        division,
        teams,
        options,
        activeTab,
        isLoading,
      }
    }
  }
</script>