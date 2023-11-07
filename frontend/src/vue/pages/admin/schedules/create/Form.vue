<template>
  <div class="relative mb-[4rem]">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="scheduleIsCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Schedule has been successfully created!
      </div>
    </div>
    
    <div class="max-w-[800px] mx-auto">
      <form @submit.prevent="createSchedule" class="form-1 p-[1em] relative">
        <div 
          v-if="isLoading"
          class="loading-2 flex justify-center items-center"
        >
          <LoadingSpinner />
        </div>
        
        <div class="non-field-errors mb-[1rem]">
          <Errors
            :errors="errors.non_field_errors"
          />
        </div>

        <div class="mb-[1rem]">
          <select
            class="input-field-3"
            v-model="schedule.season"
            name="season"
            id="season"
            required="required"
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

          <Errors 
            :errors="errors.season"
          />
        </div>

        <div class="mb-[1rem]">
          <select
            v-model="schedule.division"
            class="input-field-3"
            name="division"
            id="division"
            required="required"
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

          <Errors 
            :errors="errors.division"
          />
        </div>

        <div class="mb-[1rem]">
          <select
            v-model="schedule.game_type"
            class="input-field-3"
            name="division"
            id="division"
            required="required"
          >
            <option value="" disabled selected>Select Game Type</option>
            <option value="E">Eliminations</option>
            <option value="P">Playoffs</option>
            <option value="F">Finals</option>
          </select>

          <Errors 
            :errors="errors.game_type"
          />
        </div>

        <div class="mb-[1rem]">
          <input
            v-model="schedule.date"
            class="input-field-3"
            type="datetime-local"
            name="date"
            id="date"
            required="required"
          />
          <Errors 
            :errors="errors.date"
          />
        </div>

        <div class="mb-[1rem]">
          <input
            v-model="schedule.venue"
            class="input-field-3"
            type="text"
            name="venue"
            id="venue"
            placeholder="Enter Venue"
            required="required"
          />

          <Errors 
            :errors="errors.venue"
          />
        </div>

        <div class="mb-[1rem]">
          <select
            v-model="schedule.home_team"
            class="input-field-3"
            name="home_team"
            id="home_team"
            required="required"
          >
            <option value="" disabled selected>Select Home Team</option>
            <option
              v-for="team in teamOptions"
              :key="team.id"
              :value="team.id"
            >
              {{ team.name }}
            </option>
          </select>

          <Errors 
            :errors="errors.home_team"
          />
        </div>

        <div>
          <select
            v-model="schedule.away_team"
            class="input-field-3"
            name="away_team"
            id="away_team"
          >
            <option value="" disabled selected>Select Away Team</option>
            <option
              v-for="team in teamOptions"
              :key="team.id"
              :value="team.id"
            >
              {{ team.name }}
            </option>
          </select>

          <Errors 
            :errors="errors.away_team"
          />
        </div>
        <div class="text-right">
          <button class="btn-7 mt-[1rem]">Create Schedule</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import { computed, reactive, ref, watch } from 'vue';
  import axios from 'axios';
  import host from '@composables/host.js';
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import Errors from './Errors.vue';

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    name: 'Form',
    components: {
      Errors,
      LoadingSpinner
    },
    setup() {
      const options = ref({})
      const scheduleIsCreated = ref(false)
      const errors = ref({})
      const isLoading = ref(false)
      const hasError = error()
      const schedule = reactive({
        division: '',
        home_team: '',
        away_team: '',
        season: '',
        date: '',
        venue: '',
        game_type: '',
      })
      const url = host + '/api/game-schedule/options/'

      /**
       * Computed
       */
        const teamOptions = computed(() => {
          if (schedule.division === 'J') {
            return options.value.junior_division_teams
          } else if (schedule.division === 'S') {
            return options.value.senior_division_teams
          } else {
            // do nothing
          }
        })
      /**
       * End of Computed
       */
      
      /**
       * Methods
       */
        const getOptions = (url) => {
          isLoading.value = true
          axios
          .get(url)
          .then(response => {
            options.value = response.data
            schedule.season = response.data.season.id
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
        }

        const createSchedule = () => {
          isLoading.value = true

          const url = host + '/api/game-schedule/options/'

          axios
            .post(url, schedule)
            .then(response => {
              scheduleIsCreated.value = true;
              
              const dontEditKeys = ['season', 'division', 'game_type']
              
              for (const key in schedule) {
                if (dontEditKeys.includes(key) ) {
                  continue;
                }

                schedule[key] = ''
              }
              errors.value = {}
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              
              if (err.request.status === 400) {
                errors.value = err.response.data
                return
              }

              hasError.value = true
            })
        }
      /**
       * End of Methods
       */

        /**
       * Watch
       */
        watch(
          scheduleIsCreated,
          (isCreated) => {
            if (isCreated) {
              setTimeout(() => {
                scheduleIsCreated.value = false
              }, 5000)
            }
          }
        )

        watch(
          () => schedule.season,
          (newVal, oldVal) => {
            if (newVal == oldVal || oldVal == '') { return }
            
            let optionUrl = url
            if (schedule.season != '') {
              optionUrl += `?season=${schedule.season}`
            }

            getOptions(optionUrl)
          },
          {
            immediate: true
          }
        )
      /**
       * End Of Watch
       */

      return {
        options,
        teamOptions,
        schedule,
        scheduleIsCreated,
        errors,
        hasError,
        isLoading,
        createSchedule,
      }
    }
  }
</script>