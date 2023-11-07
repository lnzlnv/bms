<template>
  <div class="mx-[10vw]">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <h1 class="schedule__title bg-skew-2 w-max mb-[2rem]">
      GAMES TODAY
    </h1>

    <table class="table-1">
      <thead>
        <tr>
          <th class="table-1__header text-left">Match</th>
          <th class="table-1__header text-left">Date</th>
          <th class="table-1__header text-left">Time</th>
          <th class="table-1__header text-left">Venue</th>
          <th class="table-1__header text-left">Division</th>
          <th class="table-1__header text-left"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="game in games.results"
          :key="game.id"
          class="table-1__row flex flex-col lg:table-row"
        >
          <td
            class="table-1__data text-left lg:table-cell lg"
            data-cell="Match"
          >
            <div class="md:flex items-center gap-[20px]">
              <div class="flex items-center gap-[10px]">
                <img
                  class="img-6"
                  :src="game.home_team.logo"
                  alt=""
                />
                <p class="text-[2rem] font-[600]">{{ game.home_team.name }}</p>
              </div>
              
              <p class="text-2 text-[2rem] font-[600]">vs</p>
              <div class="flex items-center gap-[10px]">
                <img
                  class="img-6"
                  :src="game.away_team.logo"
                  alt=""
                />
                <p class="text-[2rem] font-[600]">{{ game.away_team.name }}</p>
              </div>
            </div>
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Date"
          >
            {{ game.date_format_1 }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Time"
          >
            {{ game.time }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Venue"
          >
            {{ game.venue }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Division"
          >
            {{ game.division }}
          </td>
          <td
            class="table-1__data empty text-left lg:table-cell"
          >
            <div>
              <a 
                class="btn-9 min-w-[100%] block text-center"
                :href="game.officiate_url"
              >
                Officiate
              </a>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="text-center mt-[2rem]">
      <div>
        <button 
          v-if="games.previous"
          @click="previous(gamesUrl)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button 
          v-if="games.next"
          @click="next(gamesUrl)"
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
  import { computed, onBeforeMount, ref, watch } from 'vue';

  import { error } from '@pages/admin/teams/create/composables.js'
  import  { page } from '@pages/admin/teams/all/composables.js'
 
  import setCsrfToken from '@composables/csrf-token.js';
  import host from '@composables/host.js';

  setCsrfToken()

  export default {
    setup() {
      const games = ref({})
      const options = ref({})
      const hasError = error()

      onBeforeMount(() => {
        const url = host + '/api/all-games/options/'

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            getGames(gamesUrl.value)
          })
          .catch(err => {
            console.log(err)
            hasError.value = true
          })
      })

      const gamesUrl = computed(() => {
        return host 
          + '/api/games/' 
          + `?limit=${limit}&offset=${limit * pageNumber.value}`
      })

      const getGames = () => {
        axios
          .get(gamesUrl.value)
          .then(response => {
            games.value = response.data
          })
          .catch(err => {
            hasError.value = true
          })
      }

      const { pageNumber, limit, next, previous } = page(getGames)

      return {
        games,
        options,
        next,
        previous,
        gamesUrl,
        hasError
      }
    }
  }
</script>