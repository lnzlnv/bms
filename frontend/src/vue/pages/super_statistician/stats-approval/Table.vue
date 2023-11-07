<template>
  <div class="mx-[10vw] relative">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div
      v-if="gameIsDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Game has been successfully deleted!
      </div>
    </div>

    <h1 class="schedule__title bg-skew-2 w-max mb-[2rem]">
      Game Stats Approval
    </h1>

    <table class="table-1">
        <thead>
          <tr>
            <th class="table-1__header text-left">Match</th>
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
              class="table-1__data text-left lg:table-cell"
              data-cell="Match"
            >
              <div class="flex items-center gap-[10px] flex-wrap">
                <div class="flex items-center gap-[5px] flex-wrap">
                  <img
                    class="img-6"
                    :src="game.home_team.logo"
                    alt=""
                  />
                  <p class="text-[2rem] font-[600]">{{ game.home_team.name }}</p>
                </div>
                <span>vs</span>
                <div class="flex items-center gap-[5px] flex-wrap">
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
              data-cell="Match"
            >
              {{ game.home_team.division }}
            </td>
            <td
              class="table-1__data empty text-left lg:table-cell"
            >
              <div class="grid grid-2-column-2 gap-[10px]">
                <a 
                  class="btn-9 text-center"
                  :href="game.reports_url"
                >
                  View Report
                </a>
                <button
                  @click="deleteGame(game.id)"
                  class="btn-10"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="text-center mt-[2rem]">
        <div>
          <button
            v-if="games.previous"
            @click="previous(gamesForApprovalAPIUrl)"
            class="btn-11 mr-[0.5rem]"
          >
            Prev
          </button>
          <button
            v-if="games.next"
            @click="next(gamesForApprovalAPIUrl)"
            class="btn-11"
          >
            Next
          </button>
        </div>
      </div>
  </div>
</template>

<script>
  import host from '@composables/host.js';
  import { computed, onBeforeMount, ref, watch } from 'vue';
  import axios from 'axios';

  import { error } from '@pages/admin/teams/create/composables.js'
  import  { page } from '@pages/admin/teams/all/composables.js'

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    setup() {
      const options = ref({})
      const season = ref('')
      const division = ref('J')
      const games = ref({})
      const gameIsDeleted = ref(false)
      const hasError = error()

      onBeforeMount(() => {
        const url = host + '/api/games-approval-options/'

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            season.value = response.data.current_season.id
          })
          .catch(err => {
            console.error(err)
            hasError.value = true
          })
      })
      
      /**
       * Computed
       */
        const gamesForApprovalAPIUrl = computed(() => {
          return host 
            + '/api/games-stats-approval/division/' 
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */


      /**
       * Watch
       */
        watch(
          season,
          () => {
            getGamesToBeApproved(gamesForApprovalAPIUrl.value)
          }
        )

        watch(
          division,
          () => {
            getGamesToBeApproved(gamesForApprovalAPIUrl.value)
          }
        )

        watch(
          gameIsDeleted,
          (isDeleted) => {
            if (isDeleted) {
              setTimeout(() => {
                gameIsDeleted.value = false
              }, 5000)
            }
          }
        )
      /**
       * Enf of Watch
       */
      
      /**
       * Methods
       */
        const getGamesToBeApproved = (url) => {
            axios
              .get(url)
              .then(response => {
                games.value = response.data
              })
              .catch(err => {
                console.error(err)
                hasError.value = true
              })
        }

        const deleteGame = (id) => {
          const url = host + '/api/games-stats-approval/' + id + '/'

          axios 
            .delete(url)
            .then(response => {
              gameIsDeleted.value = true
              getGamesToBeApproved(gamesForApprovalAPIUrl.value)
            })
            .catch(err => {
              console.error(err)
              hasError.value = true
            })
        }
      /**
       * End of Methods
       */

      const { pageNumber, limit, next, previous } = page(getGamesToBeApproved)
        
      return {
        options,
        division,
        season,
        games,
        gameIsDeleted,
        deleteGame,
        getGamesToBeApproved,
        hasError,
        next,
        previous,
        gamesForApprovalAPIUrl
      }
    }
  }
</script>