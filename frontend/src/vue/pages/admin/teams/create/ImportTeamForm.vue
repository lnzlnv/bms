<template>
  <div>
    <div 
      v-if="isImported"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Team has been successfully imported!
      </div>
    </div>

    <div class="mb-[1rem] md:flex justify-between items-center">
      <button
        @click="activeTab = 1"
        class="btn-12 mb-[1rem] md:mb-0"
      >
        Add Team
      </button>

      <form class="md:flex justify-end items-start gap-[20px]">
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

    <form
      @submit.prevent="importTeamAPICall"
      class="form-1 p-[1em] relative" 
      id="js-form-1"
    >
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

      <div>
        <input 
          v-model="isSelectAll"
          class="input-checkbox-2"
          type="checkbox" 
          id="select_all"
        >
        <label  
          class="label-checkbox-1 flex items-center gap-[10px] mb-[1rem]"
          for="select_all"
        >
          Select All
        </label>
      </div>

      <div 
        v-for="team in teams"
        :key="team.id"
      >
        <input 
          class="input-checkbox-2 js-checkbox"
          type="checkbox" 
          :name="'team-' + team.id" 
          :id="'team-' + team.id"
          @change="importTeam($event, team.id)"
        >
        <label 
          class="label-checkbox-1 flex items-center gap-[10px]"
          :for="'team-' + team.id"
        >
          {{ team.name }}
        </label>
      </div>

      <div class="text-right">
        <button class="btn-7">Import Teams</button>
      </div>
    </form>
  </div>
</template>
<script>
  import { computed, inject, onBeforeMount, onUpdated, ref, watch } from 'vue';
  import Errors from '@pages/admin/schedules/create/Errors.vue'; 
  import axios, { all } from 'axios';
  import normalizeData from '@composables/normalize-data-4.js'
  import success from "@composables/generate-account/success.js"
  import LoadingSpinner from '@templates/LoadingSpinner.vue';

  export default {
    components: {
      Errors,
      LoadingSpinner
    },
    setup() {
      const errors = ref({})
      const isSelectAll = ref(false)
      const allTeams = ref([])
      const season = ref('')
      const division = ref('J')
      const options = inject('options', options)
      const activeTab = inject('activeTab', activeTab)
      const hasError = inject('hasError', hasError)
      const isLoading = inject('isLoading', isLoading)
      let isUnselected = false
      let selectedTeams = {}
      let form1 = null;
      let teamsCheckboxes = []
      const isImported = success()

      onBeforeMount(() => {
        const url = '/api/teams/import/'
      })

      onUpdated(() => {
        if (Object.keys(teams.value).length == 0) { 
          form1 = document.getElementById('js-form-1')
          return 
        }
        
        teamsCheckboxes = form1.querySelectorAll('.js-checkbox')
      })

      /**
       * Watch
       */
        watch(
          isSelectAll,
            (isAll) => {
              if (isAll) {
                selectAll(true)
                addAllToSelectedTeams()
                isUnselected = false
              } else if (!isAll && !isUnselected) {
                selectAll(false)
                selectedTeams = {}
              } else {
                // do nothing
              }
            }
          )
        
        watch(
          options,
          () => {
            season.value = options.value.seasons[0].id
          }
        )

        watch(
          [season],
          () => {
            isLoading.value = true
            const url = '/api/teams/import/'
              + season.value 
              + '/'
            
            axios
              .get(url)
              .then(response => {
                allTeams.value = normalizeData(response.data)
                isSelectAll.value = false
                isLoading.value = false
              })
              .catch(err => {
                isLoading.value = false
                hasError.value = true
              })
          }
        )
      /**
       * End of Watch
       */

      /**
       * Computed
       */
        const teams = computed(() => {
          const filteredTeams = Object.fromEntries(Object.entries(
            allTeams.value).filter(
              ([key, value]) => value.division == division.value
            )
          )
          return filteredTeams
        })
      /**
       * End of Computed
       */

      /**
       * Methods
       */
        const selectAll = (value) => {
          for (let i = 0; i < teamsCheckboxes.length; ++i){
            teamsCheckboxes[i].checked = value
          }
        }

        const addAllToSelectedTeams = () => {
          for(const team in teams.value) {
            selectedTeams[teams.value[team].id] = teams.value[team].id
          }
        }

        const importTeam = (event, teamId) => {
          const isSelected = event.target.checked
          if (isSelected) {
            selectedTeams[teamId] = teamId
          } else {
            delete selectedTeams[teamId]
            isUnselected = true
          }
          setSelectAllPlayers()
        }

        const setSelectAllPlayers = () => {
          const numberOfTeams = Object.keys(teams.value).length
          const numberOfSelectedTeams =  Object.keys(selectedTeams).length
          const allIsSelected = numberOfSelectedTeams == numberOfTeams
          isSelectAll.value = allIsSelected
        }

        const importTeamAPICall = () => {
          isLoading.value = true
          const data = {
            teams: getSelectedTeamList()
          }
          const url = '/api/teams/import/'
            + season.value
            + '/'

          axios
            .post(url, data)
            .then(response => {
              removeImportedTeams()
              isImported.value = true
              selectedTeams = {}
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              if (err.response.status != 400) {
                hasError.value = true
                return
              }
              errors = err.response.data
            })
        }

        const getSelectedTeamList = () => {
          const data = []

          for (const team in selectedTeams) {
            data.push(selectedTeams[team])
          }

          return data
        }

        const removeImportedTeams = () => {
          for (const team in selectedTeams) {
            delete allTeams.value[team]
          }
        }
      /**
       * End of Methods
       */

      return {
        errors,
        isSelectAll,
        options,
        season,
        activeTab,
        division,
        teams,
        isImported,
        isLoading,
        importTeam,
        importTeamAPICall
      }
    }
  }
</script>