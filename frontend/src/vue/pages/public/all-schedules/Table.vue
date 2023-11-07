<template>
  <div class="p-[1em] lg:mx-[10vw]">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="isLoading"
      class="loading-3 flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <table class="table-1">
      <thead>
        <tr>
          <th class="table-1__header text-left">Match</th>
          <th class="table-1__header text-left">Division</th>
          <th class="table-1__header text-left">Date</th>
          <th class="table-1__header text-left">Time</th>
          <th class="table-1__header text-left">Venue</th>
        </tr>
      </thead>
      <tbody v-if="allGameSchedules.results && allGameSchedules.results.length != 0">
        <tr
          v-for="schedule in allGameSchedules.results"
          :key="schedule.id"
          class="table-1__row flex flex-col lg:table-row"
        >
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Match"
          >
            <div class="flex items-center gap-[10px]">
              <div class="flex items-center gap-[10px]">
                <img
                  class="img-6"
                  :src="schedule.home_team.logo"
                  alt="home team logo"
                >
                <p>{{ schedule.home_team.name }}</p>
              </div>
              <p class="font-bold">vs</p>
              <div class="flex items-center gap-[10px]">
                <img
                  class="img-6"
                  :src="schedule.away_team.logo"
                  alt="away team logo"
                >
                <p>{{ schedule.away_team.name }}</p>
              </div>
            </div>
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Division"
          >
            {{ schedule.home_team.division }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Date"
          >
            {{ schedule.date_format }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Time"
          >
            {{ schedule.time }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Venue"
          >
            {{ schedule.venue }}
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr class="table-1__row flex flex-col lg:table-row">
          <td class="table-1__data lg:table-cell" colspan="5">No available schedules.</td>
        </tr>
      </tbody>
    </table>

    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-if="allGameSchedules.previous"
          @click="previous(url)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-if="allGameSchedules.next"
          @click="next(url)"
          class="btn-11"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { computed, onBeforeMount, ref } from 'vue';
  import { error } from '@pages/admin/teams/create/composables.js'
  import  { page } from '@pages/admin/teams/all/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  export default {
    components: {
      LoadingSpinner
    },
    setup() {
      const allGameSchedules = ref({})
      const division = ref('J')
      const hasError = error()
      const isLoading = ref(false)
      
      onBeforeMount(() => {
        getSchedules(url.value)
      })

      /**
       * Computed
       */
        const url = computed(() => {
          return '/api/public/schedules/all/'
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */

      /**
       * Methods
       */
        const getSchedules = (url) => {
          isLoading.value = true

          axios
          .get(url)
          .then(response => {
            allGameSchedules.value = response.data
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
        }
      /**
       * End of Methods
       */

      const { pageNumber, limit, next, previous } = page(getSchedules)

      return {
        hasError,
        allGameSchedules,
        division,
        url,
        next,
        previous,
        isLoading
      }
    }
  }
</script>