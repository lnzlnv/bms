<template>
  <div class="container-7 relative">
    <div 
      v-if="isLoading"
      class="loading-2 flex justify-center items-center"
    >
      <LoadingSpinner />
    </div>
    <div class="text-right mb-[1rem]">
      <button
        @click="closeModal"
      >
        <img 
        class="icon-2"
        :src="closeIcon" 
        alt="close icon"
      />
      </button>
    </div>

    <form @submit.prevent="updateSchedule">
      <div class="non-field-errors mb-[1rem]">
        <Errors
          :errors="errors.non_field_errors"
        />
      </div>

      <div>
        <select
          v-model="schedule.season"
          class="input-field-3 mb-[1rem]"
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
          type="datetime-local" 
          class="input-field-3"
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
          :errors="errors.home_team_id"
        />
      </div>
      <div>
        <select
          v-model="schedule.away_team"
          class="input-field-3"
          name="away_team"
          id="away_team"
          required="required"
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
          :errors="errors.away_team_id"
        />
      </div>
      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Edit Schedule</button>
      </div>
    </form>
  </div>
</template>

<script>
  import { computed, onBeforeMount, reactive, ref, inject } from 'vue';
  import axios from 'axios';
  import host from '@composables/host.js';
  import closeIcon from '@images/close-icon.svg'
  import Errors from '@pages/admin/schedules/create/Errors.vue'; 
  import LoadingSpinner from '@templates/LoadingSpinner.vue';

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    name: 'Form',
    components: {
    Errors,
    LoadingSpinner
},
    props: {
      closeModal: Function,
      editSuccess: Function,
      selectedSchedule: {},
      options: {},
      gameSchedule: {},
      season: Number,
      division: String
    },
    setup(props) {
      const isLoading = ref(false)
      const errors = ref({})
      const getSchedules = inject('getSchedules', getSchedules)
      const allScheduleUrl = inject('allScheduleUrl', allScheduleUrl)
      const schedule = reactive({})

      const closeModal = () => {
        props.closeModal()
      }

      onBeforeMount(() => {
        for (const key in props.selectedSchedule) {
          schedule[key] = props.selectedSchedule[key]
        }
        schedule['home_team'] = props.selectedSchedule['home_team'].id
        schedule['away_team'] = props.selectedSchedule['away_team'].id
      })

      const teamOptions = computed(() => {
        if (schedule.division === 'J') {
          return props.options.junior_division_teams
        } else if (schedule.division === 'S') {
          return props.options.senior_division_teams
        } else {
          // do nothing
        }
      })

      const updateSchedule = () => {
        isLoading.value = true

        const url = host + '/api/game-schedule/edit/' + props.selectedSchedule.id + '/'
        const scheduleData = {
          division: schedule.division,
          home_team_id: schedule.home_team,
          away_team_id: schedule.away_team,
          season: schedule.season,
          date_local: schedule.date,
          venue: schedule.venue,
          game_type: schedule.game_type
        }

        axios
          .post(url, scheduleData)
          .then(response => {
            props.closeModal()
            isLoading.value = false

            const newSchedule = response.data
            const results = props.gameSchedule.results;
            const scheduleId = schedule.id
            const newSeason = schedule.season
            const newDivision = schedule.division

            if (newSeason != props.season || newDivision != props.division) {
              getSchedules(allScheduleUrl.value)
            }

            for(let i = 0; i < props.gameSchedule.results.length; ++i) {
              if(props.gameSchedule.results[i].id != scheduleId) {
                continue
              }

              for (const key in newSchedule) {
                if (results[i][key] != undefined) {
                  props.gameSchedule.results[i][key] = newSchedule[key]
                }
              }

              break
            } 

            props.editSuccess()
            errors.value = {}
          })
          .catch(err => {
            isLoading.value = false
            if (err.request == undefined || err.request.status != 400) {
              hasError.value = true
              return
            }

            errors.value = err.response.data
          })
      }

      const hasError = inject('hasError', hasError)

      return {
        closeIcon,
        ...props,
        teamOptions,
        errors,
        schedule,
        isLoading,
        closeModal,
        updateSchedule,
      }
    }
  }
</script>