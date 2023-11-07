<template>
  <div>
    <div 
      v-if="modalIsOpen"
      class="modal-1 flex items-center"
    >
      <EditForm 
        :options="options"
        :selectedTeam="selectedTeam"
        :isEdited="isEdited"
      />
    </div>
    <div 
      v-if="isLoading"
      class="loading flex justify-center"
    >
      <LoadingSpinner />
    </div>
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
        v-if="teamIsEdited"
        class="container-6 flex justify-center"
      >
        <div class="success-1">
          Team has been successfully edited!
        </div>
      </div>

      <div
          v-if="teamIsDeleted"
          class="container-6 flex justify-center"
        >
          <div class="delete-1">
            Team has been successfully deleted!
          </div>
        </div>

      <div class="mb-[1rem] md:grid grid-3-column-1 items-end">
        <div> 
          <a href="/teams/create/">
            <button class="btn-12">Add Team</button>
          </a>
        </div>

        <div class="label-2 text-center mb-[1rem] md:mb-[0]">
          Please click team to view players.
        </div>

        <form class="md:flex justify-end items-start gap-[20px]">
          <div class="grid grid-2-column-3">
            <select
              v-model="season"
              class="input-field-5"
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
          <div class="grid grid-2-column-3">
            <select
              v-model="division"
              class="input-field-5"
              name="division"
              id="division"
            >
              <option value="" disabled selected>Select Division</option>
              <option
                v-for="division in options.divisions"
                :key="division[0]"
                :value="division[0]"
              >
                {{ division[1] }}
              </option>
            </select>
          </div>
        </form>
      </div>

      <div>
        <div
          v-if="teams.results && teams.results.length != 0"
          class="lg:grid grid-container-8 gap-[10px]"
        >
          <div
            v-for="team in teams.results"
            :key="team.id"
            class="mb-[1rem] lg:mb-0"
          >
            <a :href="team.players_url">
              <div class="mb-[1rem]">
              <img
                class="img-15 mx-[auto]"
                :src="typeof team.logo == 'object'?  windowObj.URL.createObjectURL(team.logo) : team.logo"
                alt=""
              >
              <div class="text-1 text-center">
                {{ team.name }}
              </div>
            </div>
            </a>
        
            <div class="grid grid-2-column-2 gap-[10px]">
              <button
                @click="selectTeam(team.id)"
                class="btn-9"
              >
                Edit
              </button>
              <button
                @click="deleteTeam(team.id)"
                class="btn-10"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
        <p
          v-else
          class="text-1 text-center"
        >
          No available teams.
        </p>
      </div>

      <div class="text-center mt-[2rem]">
        <div>
          <button
            v-if="teams.previous"
            @click="previous(teamUrl)"
            class="btn-11 mr-[0.5rem]"
          >
            Prev
          </button>
          <button
            v-if="teams.next"
            @click="next(teamUrl)"
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
  import axios from 'axios';
  import { computed, onBeforeMount, ref, watch, provide } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import setCsrfToken from '@composables/csrf-token.js';
  import host from '@composables/host.js';
  import EditForm from './EditForm.vue'
  import success from '@composables/generate-account/success.js'
  import { page } from './composables.js'

  setCsrfToken()

  export default {
    components: {
      EditForm,
      LoadingSpinner
    },
    setup() {
      const teams = ref({})
      const options = ref({})
      const division = ref('J')
      const season = ref('')
      const teamIsDeleted = success()
      const teamIsEdited = success()
      const selectedTeam = ref({})
      const modalIsOpen = ref(false)
      const windowObj = ref(window);
      const hasError = success()
      const isLoading = ref(false)
      
      onBeforeMount(() => {
        isLoading.value = true
        const optionsUrl = host + '/api/teams/create/options/'

        axios
          .get(optionsUrl)
          .then(response => {
            options.value = response.data
            season.value = response.data.seasons[0].id
            getTeams(teamUrl.value)
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
          [division, season],
          () => {
            pageNumber.value = 0
            getTeams(teamUrl.value)
          }
        )
      /**
       * End of Watch
       */

      /**
       * Computed
       */
        const teamUrl = computed(() => {
          return host 
            + '/api/teams/' 
            + season.value
            + '/'
            + division.value 
            + '/all/'
            + `?limit=${limit}&offset=${limit*pageNumber.value}`
        })
      /**
       * End of Computed
       */
      
      /**
       * Methods
       */
        const getTeams = (url) => {
          isLoading.value = true
          axios
            .get(url)
            .then(response => {
              teams.value = response.data
              isLoading.value = false
            })
            .catch(err => {
              hasError.value = true
              isLoading.value = false
            })
        }

        const deleteTeam = (id) => {
          isLoading.value = true
          const url = host 
            + '/api/teams/' 
            + id 
            + '/'
            + `?season=${season.value}`
            
          axios
            .delete(url)
            .then(response => {
              teamIsDeleted.value = true
              getTeams(teamUrl.value)
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const selectTeam = (id) => {
          modalIsOpen.value = true

          for(let i = 0; i < teams.value.results.length; ++i) {
            if (teams.value.results[i].id == id) {
              selectedTeam.value = teams.value.results[i]
              break
            }
          }
        }

        const isEdited = () => {
          teamIsEdited.value = true
          modalIsOpen.value = false
          
          if (division.value != selectedTeam.value.division) {
            const id = selectedTeam.value.id

            for(let i = 0; i < teams.value.results.length; ++i) {
              if(teams.value.results[i].id != id) {
                continue
              }

              teams.value.results.splice(i, 1)
              break
            } 

            return;
          }
        }
      /**
       * End of Methods
       */

      provide('modalIsOpen', modalIsOpen)
      provide('hasError', hasError)

      const { pageNumber, limit, next, previous } = page(getTeams)

      return {
        teams,
        division,
        options,
        teamIsDeleted,
        teamIsEdited,
        season,
        hasError,
        modalIsOpen,
        selectedTeam,
        windowObj,
        pageNumber,
        teamUrl,
        isLoading,
        next,
        previous,
        getTeams,
        deleteTeam,
        selectTeam,
        isEdited,
      }
    }
  }
</script>