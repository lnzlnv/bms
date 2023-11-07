<template>
  <div 
    v-if="hasError"
    class="container-6 flex justify-center z-[1000000000000]"
  >
    <div class="delete-1">
      An error occured!
    </div>
  </div>

  <div class="container-2 flex justify-evenly overflow-hidden mb-[2.875rem]">
    <div 
      v-for="team in teams"
      :key="team.id"
      class="px-[0.5em]"
    >
      <img
        class="img-1 mx-0"
        :src="team.team.logo" 
      >
    </div>
  </div>

  <div class="px-[1em] mb-[2rem] relative lg:px-[5vw]">
    <div 
      v-if="isLoading"
      class="loading-3 flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <form class="md:flex justify-end gap-[20px] md:-w-max md:ml-auto">
        <select
          v-model="season"
          class="input-field-1 filter mb-[1rem] md:mb-0"
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

        <select
          v-model="division"
          class="input-field-1 filter"
          name="division"
          id="division"
        >
          <option value="" disabled selected>Select Division</option>
          <option value="J">Junior</option>
          <option value="S">Senior</option>
        </select>
    </form>

    <div class="scroll-container overflow-x-auto">
      <table class="table-1 mt-[2rem]">
        <thead>
          <tr>
            <th class="table-1__header">RANK</th>
            <th class="table-1__header lg">NAME</th>
            <th class="table-1__header">W</th>
            <th class="table-1__header">L</th>
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
              class="table-1__data grid grid-2-column-1 gap-[40px] lg:table-cell"
              data-cell="RANK"
            >
              {{ index + 1 }}
            </td>
            <td
              class="table-1__data grid grid-2-column-1 gap-[40px] lg:table-cell"
              data-cell="NAME"
            >
              {{ team.team.name }}
            </td>
            <td
              class="table-1__data grid grid-2-column-1 gap-[40px] lg:table-cell"
              data-cell="W"
            >
              {{ team.win }}
            </td>
            <td
              class="table-1__data grid grid-2-column-1 gap-[40px] lg:table-cell"
              data-cell="L"
            >
              {{ team.lose }}
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr class="table-1__row flex flex-col lg:table-row">
            <td
              class="table-1__data grid grid-2-column-1 gap-[40px] lg:table-cell"
              colspan="4"
            >
              No available standings.
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
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  export default {
    name: 'Table',
    components: {
      LoadingSpinner
    },
    setup() {
      const options = ref({})
      const season = ref(null)
      const division = ref('J')
      const allTeams = ref([])
      const hasError = error()
      const isLoading = ref(false)
      
      onBeforeMount(() => {
        isLoading.value = true
        const url = '/api/public/players/options/'

        axios
          .get(url)
          .then(response => {
            isLoading.value = false
            options.value = response.data
            season.value = response.data.current_season.id
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
          season,
          () => {
            getTeams()
          }
        )
      /**
       * End of Watch
       */

      /**
       * Methods
       */
        const getTeams = () => {
          isLoading.value = true
          const url = '/api/public/standings/all/'
            + season.value
            + '/'
            + `?standing_type=ELIMINATIONS`

          axios
            .get(url)
            .then(response => {
              isLoading.value = false
              allTeams.value = response.data
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }
      /**
       * End of Methods
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
       * End of Computed
       */

      return {
        options,
        season,
        division,
        hasError,
        teams,
        isLoading,
      }
    }
  }
</script>