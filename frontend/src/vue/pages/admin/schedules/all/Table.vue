<template>
  <div> 
    <div 
      v-if="modalIsOpen"
      class="modal-1 flex items-center"
    >
      <EditForm 
        :closeModal="closeModal"
        :selectedSchedule="selectedSchedule"
        :options="options"
        :gameSchedule="gameSchedule"
        :season="season"
        :division="division"
        :editSuccess="editSuccess"
      />
    </div>

    <div 
      v-if="isLoading"
      class="loading flex justify-center"
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
      v-if="scheduleIsEdited"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Schedule has been successfully edited!
      </div>
    </div>

    <div
      v-if="scheduleIsDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Schedule has been successfully deleted!
      </div>
    </div>

    <div class="mx-[10vw] relative">
      <div class="md:grid grid-2-column-2 items-center mb-[1rem]">
        <div class="mb-[1rem] md:mb-0">
          <a href="/schedules/create/">
            <button class="btn-12">Add Schedule</button>
          </a>
        </div>

        <form class="flex justify-end items-start gap-[20px] mb-[1rem] md:mb-0">
          <div class="mb-[1rem] md:mb-0">
            <select
              v-model="season"
              class="input-field-5 w-full"
              name="season"
              id="season"
            >
              <option value="" disabled selected>Select Season</option>
              <option
                v-for="season in seasons"
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
      <table class="table-1">
        <thead>
          <tr>
            <th class="table-1__header text-left">Match</th>
            <th class="table-1__header text-left">Date</th>
            <th class="table-1__header text-left">Time</th>
            <th class="table-1__header text-left">Venue</th>
            <th class="table-1__header text-left">Created By</th>
            <th class="table-1__header text-left"></th>
          </tr>
        </thead>
        <tbody
          v-if="gameSchedule.results && gameSchedule.results.length != 0"
        >
          <tr
            v-for="schedule in gameSchedule.results"
            :key="schedule.id"
            class="table-1__row flex flex-col lg:table-row"
          >
            <td
              class="table-1__data text-left lg:table-cell"
              data-cell="Match"
            >
              {{ schedule.match }}
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
            <td
              class="table-1__data text-left lg:table-cell"
              data-cell="Created By"
            >
              {{ schedule.creator }}
            </td>
            <td
              class="table-1__data empty text-left lg:table-cell"
            >
              <div class="grid grid-2-column-2">
                <button
                  @click="editSchedule(schedule.id)"
                  class="btn-9 mr-[0.5rem] text-center"
                >
                  Edit
                </button>
                <button
                  @click="deleteSchedule(schedule.id)"
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
              colspan="6"
            >
              No available schedules.
            </td>
          </tr>
        </tbody>
      </table>
      <div class="text-center mt-[2rem]">
        <div>
          <button
            v-if="gameSchedule.previous"
            @click="previous(allScheduleUrl)"
            class="btn-11 mr-[0.5rem]"
          >
            Prev
          </button>
          <button
            v-if="gameSchedule.next"
            @click="next(allScheduleUrl)"
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
  import  { page } from '@pages/admin/teams/all/composables.js'
  import EditForm from './EditForm.vue'
  import success from '@composables/generate-account/success.js'

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    name: 'Table',
    components: {
      EditForm,
      LoadingSpinner
    },
    setup() {
      const gameSchedule = ref({})
      const season = ref('')
      const division = ref('J')
      const seasons = ref([])
      const isLoading = ref(false)
      const options = ref({})
      const modalIsOpen = ref(false)
      const selectedSchedule = ref(null)
      const scheduleIsDeleted = success()
      const scheduleIsEdited = success()
      const hasError = success()
      const mainUrl = '/api/game-schedule/options/'

      onBeforeMount(() => {
        getOptions(mainUrl)
      })

      /**
       * Methods
       */
        const getOptions = (url) => {
          axios
            .get(url)
            .then(response => {
              options.value = response.data
              season.value = response.data.season.id
              seasons.value = response.data.seasons
            })
            .catch(err => {
              hasError.value = true
            })
        }

        const getSchedules = (url) => {
          isLoading.value = true
          axios
            .get(url)
            .then(response => {
              gameSchedule.value = response.data
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const deleteSchedule = (id) => {
          isLoading.value = true
          const url = '/api/game-schedule/delete/' + id + '/'

          axios
            .post(url)
            .then(response => {
              scheduleIsDeleted.value = true
              getSchedules(allScheduleUrl.value)
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const editSchedule = (id) => {
          modalIsOpen.value = true

          for(let i = 0; i < gameSchedule.value.results.length; ++i) {
            if (gameSchedule.value.results[i].id == id) {
              selectedSchedule.value = gameSchedule.value.results[i]
            }
          }
        }

        const closeModal = () => {
          modalIsOpen.value = false
        }

        const editSuccess = () => {
          scheduleIsEdited.value = true
        }
      /**
       * End of Methods
       */

      /**
       * Computed
       */
        const allScheduleUrl = computed(() => {
          return '/api/all-game-schedule/' 
            + season.value 
            + '/' 
            + division.value 
            + '/'
            + `?limit=${limit}&offset=${limit*pageNumber.value}`
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
            pageNumber.value = 0
            getOptions(mainUrl + `?season=${season.value}`)
            getSchedules(allScheduleUrl.value)
        })

        watch(
          division, 
          () => {
            pageNumber.value = 0
            getSchedules(allScheduleUrl.value)
        })
      /**
       * End of Watch
       */

      provide('getSchedules', getSchedules)
      provide('allScheduleUrl', allScheduleUrl)
      provide('hasError', hasError)

      const { pageNumber, limit, next, previous } = page(getSchedules)

      return {
        gameSchedule,
        scheduleIsDeleted,
        season,
        modalIsOpen,
        selectedSchedule,
        options,
        division,
        scheduleIsEdited,
        hasError,
        next,
        previous,
        allScheduleUrl,
        isLoading,
        seasons,
        deleteSchedule,
        editSchedule,
        closeModal,
        editSuccess,
      }
    }
  }
</script>
