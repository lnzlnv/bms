<template>
  <div class="recaps relative">
    <div 
      v-if="isLoading"
      class="loading-3 flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>
    
    <div
      v-if="gameSchedules.length > 0"
    >
      <div
        v-for="schedule in gameSchedules"
      >
        <div class="recaps__date">
          {{ schedule.formatted_date }}
        </div>
        <div class="md:grid grid-2-column-2 gap-[40px]">
          <div
            v-for="game in schedule.games"
            :key="game.id"
            class="recaps__content"
            :title="game.home_team.division + ' Division'"
          >
            <div class="lg:flex justify-center items-center gap-[20px]">
              <div class="flex justify-center items-center gap-[10px]">
                <img
                  class="recaps__img"
                  :src="game.home_team.logo"
                  alt="home team logo"
                  :title="game.home_team.name"
                />
                <p
                  :class="game.home_team.stats.total_points > game.away_team.stats.total_points ? 'winner': ''"
                  class="recaps__score"
                >
                  {{ game.home_team.stats.total_points }}
                </p>
              </div>
              <p class="recaps__vs text-center">vs</p>
              <div class="flex justify-center items-center gap-[10px]">
                <img
                  class="recaps__img"
                  :src="game.away_team.logo"
                  alt="away team logo"
                  :title="game.away_team.name"
                />
                <p
                  :class="game.home_team.stats.total_points < game.away_team.stats.total_points ? 'winner': ''"
                  class="recaps__score"
                >
                  {{ game.away_team.stats.total_points }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <p 
      v-else
      class="text-1 text-center"
    >
      No available game recaps.
    </p>
    
  </div>
</template>

<script>
  import axios from 'axios';
  import { onBeforeMount, ref } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import success from '@composables/generate-account/success.js'

  export default {
    components: {
      LoadingSpinner
    },
    setup() {
      const gameSchedules = ref([])
      const isLoading = ref(false)
      const hasError = success()

      onBeforeMount(() => {
        isLoading.value = true
        const url = '/api/recaps/'

        axios
          .get(url)
          .then(response => {
            gameSchedules.value = response.data
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      return {
        gameSchedules,
        hasError,
        isLoading
      }
    }
  }
</script>