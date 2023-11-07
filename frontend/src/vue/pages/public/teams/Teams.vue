<template>
	<div class="h-[90%] relative">
    <div 
      v-if="isLoading"
      class="loading-3 flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div class="mb-[1rem] md:flex justify-between">
      <div class="w-max ml-[1rem] mb-[1rem] md:ml-[0px] md:mb-0">
        <h1 class="schedule__title bg-skew-2 w-max pos-item-2">{{ teamsCategory }}</h1>
      </div>

      <form class="lg:mr-[2rem]">
        <select 
          v-model="division"
          class="input-field-1"
        >
          <option value="" selected disabled>Select Division</option>
          <option value="J">Junior</option>
          <option value="S">Senior</option>
        </select>
      </form>
    </div>

    <div class="h-full">
      <div class="relative z-[1000] py-[4em] lg:px-[5em] md:mx-[3.5rem] h-full">
        <div class="bg-skew md h-full"></div>
        <ul class="grid grid-container-2 justify-center gap-[40px]">
          <li v-for="team in teams" :key="team.id">
            <img
              class="img-3 mx-[auto] mb-[1rem]"
              :src="team.logo"
            />
            <p class="team__name">{{ team.name }}</p>
          </li>
        </ul>
      </div>
    </div> 
  </div>
</template>

<script>
  import { ref, computed, onBeforeMount } from 'vue'
  import axios from 'axios'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import success from '@composables/generate-account/success.js'

	export default {
    components: {
      LoadingSpinner
    },  
		setup() {
      const division = ref('J')
      const allTeams = ref([])
      const isLoading = ref(true)
      const hasError = success()

      onBeforeMount(() => {
        isLoading.value = true
        const url = '/api/teams/view/public/all/'

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
      })

      const teamsCategory = computed(() => {
        if (division.value == 'J') {
          return 'JUNIOR TEAMS'
        }
        return 'SENIOR TEAMS'
      })

      /**
       * Computed
       * */
      const teams = computed(() => {
        return allTeams.value.filter(team => team.division == division.value)
      })
      /**
       * End of Computed
       * */

			return {
				division,
        teamsCategory,
        teams,
        isLoading,
			}
		}
	}
</script>