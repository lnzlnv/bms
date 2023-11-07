<template>
  <div>
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>
      
    <div>
      <div class="container-2 flex justify-evenly mb-[2.875rem] min-h-full">
        <button
          v-for="team in teams"
          :key="team.id"
          @click="changeActiveTeam(team.id, team.name)"
          :class="team.id == activeTeam.id ? 'active' : ''"
          class="px-[0.5em] btn-6"
        > 
          <div class="overlay-1 justify-center items-center">
            {{ team.name }}
          </div>
          <img
            class="img-1 mx-0"
            :src="team.logo" 
          >
        </button>
      </div>

      <div class="px-[1em] md:px-[5vw] relative">
        <div 
          v-if="isLoading"
          class="loading-3 flex justify-center"
        >
          <LoadingSpinner />
        </div>
        <div class="flex flex-col-reverse items-start md:grid md:items-center gap-[10px] md-grid-2-column-3 md:flex-row md:justify-between">
          <h1 class="schedule__title left bg-skew-2 m-max">{{ activeTeam.name }}</h1>

          <form class="w-full md:ml-auto md:w-max md:flex gap-[10px]">
            <select 
              v-model="season"
              class="input-field-1"
            >
              <option value="" selected disabled>Select Season</option>
              <option
                v-for="season in options.seasons"
                :key="season.id"
                :value="season.id"
              >
                {{ season.year }}
              </option>
            </select>

            <select 
              v-model="division"
              class="input-field-1 mb-[1rem] md:mb-0"
            >
              <option value="" selected disabled>Select Division</option>
              <option value="J">Junior</option>
              <option value="S">Senior</option>
            </select>
          </form>
        </div>

        <table class="table-1 mt-[2rem]">
          <thead>
            <tr>
              <th class="table-1__header lg">PLAYER</th>
              <th class="table-1__header lg">NUMBER</th>
              <th class="table-1__header lg-text-right">HT</th>
              <th class="table-1__header lg-text-right">WT</th>
              <th class="table-1__header">POS</th>
            </tr>
          </thead>
          <tbody
            v-if="players.length > 0"
          >
            <tr 
              v-for="player in players"
              :key="player.id"
              class="table-1__row flex flex-col lg:table-row"
            >
              <td 
                class="table-1__data grid grid-2-column-1 gap-[10px] lg:table-cell"
                data-cell="PLAYER"
              >
                {{ player.first_name }} {{ player.last_name }}
              </td>
              <td 
                class="table-1__data grid grid-2-column-1 gap-[10px] lg:table-cell"
                data-cell="PLAYER"
              >
                {{ player.player_number }}
              </td>
              <td 
                class="table-1__data grid grid-2-column-1 gap-[10px] lg:table-cell lg-text-right"
                data-cell="HT"
              >
                {{ player.height }}
              </td>
              <td 
                class="table-1__data grid grid-2-column-1 gap-[10px] lg:table-cell lg-text-right"
                data-cell="WT"
              >
                {{ player.weight }}
              </td>
              <td 
                class="table-1__data grid grid-2-column-1 gap-[10px] lg:table-cell"
                data-cell="POS"
              >
                {{ player.position }}
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr class="table-1__row flex flex-col lg:table-row">
              <td 
                class="table-1__data empty grid grid-2-column-1 gap-[10px] lg:table-cell"
                colspan="5"
              >
                No available players.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref, onBeforeMount, computed, watch, reactive } from 'vue'
  import axios from 'axios'
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  export default {
    name: 'Table',
    components: {
      LoadingSpinner
    },
    setup() {
      const division = ref('J')
      const season = ref(null)
      const hasError = error()
      const allTeams = ref([])
      const activeTeam = reactive({
        name: null,
        id: null
      })
      const options = ref({})
      const players = ref([])
      const isLoading = ref(false)
      
      onBeforeMount(() => {
        isLoading.value = true
        const url = '/api/teams/view/public/all/'

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

        const optionsUrl = '/api/public/players/options/'

        axios
          .get(optionsUrl)
          .then(response => {
            options.value = response.data
            season.value = response.data.current_season.id
          })
          .catch(err => {
            hasError.value = true
          })

      })

      /**
       * Computed
       * */
      const teams = computed(() => {
        if (allTeams.value.length == 0) { return }

        let teamsCategory = null
        const data = {}

        if (division.value == 'J') {
          teamsCategory = allTeams.value.filter(team => team.division == 'J')
        } else {
          teamsCategory = allTeams.value.filter(team => team.division == 'S')
        }

        activeTeam['name'] = teamsCategory[0].name
        activeTeam['id'] = teamsCategory[0].id

        for (let i = 0; i < teamsCategory.length; ++i) {
          data[teamsCategory[i].name] = teamsCategory[i]
        }

        return data
      })

      /**
       * End of Computed
       * */

      /**
       * Watch
       * */
      watch(
        activeTeam,
        (value) => {
          if (season.value == null) { return }
          getPlayers()
        }
      )

      watch(
        season,
        () => {
          if (activeTeam.id == null) { return }
          getPlayers()
        }
      )
      /**
       * End of Watch
       * */

      /**
       * Methods
       * */
      const getPlayers = () => {
        isLoading.value = true
        const url = '/api/public/players/'
          + season.value
          + '/'
          + activeTeam.id
          axios
            .get(url)
            .then(response => {
              players.value = response.data
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
      }

      const changeActiveTeam = (id, name) => {
        activeTeam['id'] = id
        activeTeam['name'] = name
      }
      /**
       * End of Methods
       * */

      return {
        division,
        hasError,
        teams,
        activeTeam,
        options,
        season,
        players,
        isLoading,
        changeActiveTeam
      }
    }
  }
</script>