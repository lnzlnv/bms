<template>
  <div class="mx-[10vw] mb-[2rem]">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div
      v-if="isDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Game Report has been successfully deleted!
      </div>
    </div>

    <div 
      v-if="isLoading"
      class="loading-3 flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div class="md:flex items-center justify-between mb-[1rem]">
      <div class="mb-[1rem] md:mb-0">
        <button
          @click="activeTab = 0"
          :class="activeTab == 0? 'active': ''"
          class="btn-21"
        >
          Pending
        </button>
        <button
          @click="activeTab = 1"
          :class="activeTab == 1? 'active': ''"
          class="btn-21"
        >
          Approved
        </button>
      </div>

      <form 
        v-show="activeTab == 1"
        class="flex justify-end items-start gap-[20px] mb-[1rem] md:mb-0"
      >
        <div class="mb-[1rem] md:mb-0">
          <select
            v-model="season"
            class="input-field-5 w-full"
            name="season"
            id="season"
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
            <option value="" selected disabled>Select Division</option>
            <option value="J">Junior</option>
            <option value="S">Senior</option>
          </select>
        </div>
      </form>
    </div>

    <div>
      <table class="table-1">
        <thead>
          <tr>
            <th class="table-1__header text-left">Game</th>
            <th class="table-1__header text-left">Type</th>
            <th class="table-1__header text-left">Date</th>
            <th class="table-1__header text-left"></th>
          </tr>
        </thead>
        <tbody v-if="allGames.results && allGames.results.length != 0">
          <tr
            v-for="game in allGames.results"
            :key="game.id"
            class="table-1__row w-max flex flex-col lg:table-row"
          >
            <td
              class="table-1__data lg:w-max text-left lg:table-cell"
              data-cell="Game"
            >
              <div class="flex items-center gap-[10px] flex-wrap md:w-max">
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
              data-cell="Type"
            >
              {{ game.game_type }}
            </td>
            <td
              class="table-1__data text-left lg:table-cell"
              data-cell="Date"
            >
              {{ game.date_format_1 }}
            </td>
            <td
              class="table-1__data empty text-left lg:table-cell"
            >
              <div class="grid grid-2-column-2">
                <a
                  :href="game.admin_report_url"
                  class="btn-9 mr-[0.5rem] text-center"
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
        <tbody v-else>
          <tr class="table-1__row flex flex-col lg:table-row">
            <td
              class="table-1__data empty lg:table-cell"
              colspan="4"
            >
              <span v-show="activeTab == 0">
                No available games stats report for approval.
              </span>
              <span v-show="activeTab == 1">
                No available games stats report.
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="text-center mt-[2rem]">
        <div>
          <button
            v-if="allGames.previous"
            @click="previous(gamesUrl)"
            class="btn-11 mr-[0.5rem]"
          >
            Prev
          </button>
          <button
            v-if="allGames.next"
            @click="next(gamesUrl)"
            class="btn-11"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import { computed, onBeforeMount, provide, ref, watch } from 'vue'
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import  { page } from '@pages/admin/teams/all/composables.js'
  import axios from 'axios'

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    components: {
      LoadingSpinner,
    },
    setup() {
      const hasError = error()
      const isLoading = ref(true)
      const activeTab = ref(0)
      const isDeleted = ref(false)
      const allGames = ref({})
      const division = ref('J')
      const season = ref(0)
      const options = ref({})

      onBeforeMount(() => {
        const url = '/api/teams/create/options/'
        axios
          .get(url)
          .then(response => {
            options.value = response.data
            season.value = response.data.seasons[0].id
          })
          .catch(err => {
            hasError.value = true
          })

        
        getGames(gamesUrl.value)
      })

      const getGames = (url) => {
          isLoading.value = true
        axios
          .get(url)
          .then(response => {
            allGames.value = response.data
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      }

      const deleteGame = (id) => {
        isLoading.value = true
        const url = '/api/games-for-admin-approval/' + id + '/'
        
        axios
          .delete(url)
          .then(response => {
            isDeleted.value = true
            getGames(gamesUrl.value)
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      }

      const gamesUrl = computed(() => {
          return '/api/games-for-admin-approval/'
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
            + `&is_approved=${activeTab.value}`
            + `&season=${season.value}&division=${division.value}`
        })

      watch(
        [activeTab, division, season],
        () => {
          getGames(gamesUrl.value)
        }
      )

      watch(
          isDeleted,
          (deleted) => {
            if (deleted) {
              setTimeout(() => {
                isDeleted.value = false
              }, 5000)
            }
          }
        )

      provide('hasError', hasError)
      provide('isLoading', isLoading)
      provide('isDeleted', isDeleted)

      const { pageNumber, limit, next, previous } = page(getGames)

      return {
        activeTab,
        isLoading,
        hasError,
        isDeleted,
        allGames,
        next,
        previous,
        gamesUrl,
        division,
        options,
        season,
        deleteGame,
      }
    }
  }
</script>