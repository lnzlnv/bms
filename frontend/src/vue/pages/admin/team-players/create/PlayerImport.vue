<template>
  <div>
    <form
      class="form-1 p-[1em] relative" 
      id="js-form-1"
      @submit.prevent="importPlayersAPICall"
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
          v-model="isSelectAllPlayers"
          class="input-checkbox-2"
          type="checkbox" 
          id="select_all"
          @change="unSelectAllPlayers"
        >
        <label  
          class="label-checkbox-1 flex items-center gap-[10px] mb-[1rem]"
          for="select_all"
        >
          Select All
        </label>
      </div>

      <div
        class="mb-[0.5rem]"
        v-for="player in players"
        :key="player.id"
      >
        <input 
          class="input-checkbox-2 js-checkbox"
          type="checkbox"
          :id="`player-${player.id}`"
          @change="importPlayer($event, player.player_number)"
        >
        <label 
          class="label-checkbox-1 flex items-center gap-[10px]"
          :for="`player-${player.id}`"
        >
          {{ player.player_number }} - {{ player.first_name }} {{ player.last_name }}
        </label>
      </div>
  
      <div class="text-right">
        <button class="btn-7">Import Players</button>
      </div>
    </form>
  </div>
</template>

<script>
  import axios from 'axios';
  import { computed, inject, onBeforeMount, onMounted, onUpdated, ref, watch } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import Errors from '@pages/admin/schedules/create/Errors.vue'; 
  import normalizeData from '@composables/normalize-data-3.js'


  export default {
    components: {
      Errors,
      LoadingSpinner
    },
    setup() {
      const players = ref([])
      const options = inject('options', options)
      const teamId = ref({})
      const isSelectAllPlayers = ref(false)
      const errors = ref({})
      const hasError = inject('hasError', hasError)
      const isLoading = inject('isLoading', isLoading)
      let selectedPlayers = []
      let playersCheckboxes = []
      let form1 = null

      onBeforeMount(() => {
        teamId.value = inject('teamId', teamId)
      })

      onUpdated(() => {
        if (players.value.length == 0) { 
          form1 = document.getElementById('js-form-1')
          return 
        }
        
        playersCheckboxes = form1.querySelectorAll('.js-checkbox')
      })

      /**
       * Watch
       */
        watch(
          options,
          () => {
            isLoading.value = true
            const url = '/api/team/players/import/season-'
              + current_season.value
              + '/team-'
              + teamId.value
              + '/'

            axios
              .get(url)
              .then(response => {
                players.value = normalizeData(response.data)
                isLoading.value = false
              })
              .catch(err => {
                isLoading.value = false
                hasError.value = true
              })
          }
        )
        
        watch(
          isSelectAllPlayers,
          (isAll) => {
            if (isAll) {
              select(isAll)
              addAllToSelectedPlayers()
            }
          }
        )
      /**
       * End of Watch
       */

      /**
        * Computed
        */
        const current_season = computed(() => {
          return options.value.current_season.id
        })
      /**
        * End of Computed
        */

      /**
       * Methods
       */
        const importPlayer = (event, playerNumber) => {
          if (isSelectAllPlayers.value) {
            isSelectAllPlayers.value = false
          }

          const isSelected = event.target.checked
          if (isSelected) {
            selectedPlayers.push(players.value[playerNumber])
            
            setSelectAllPlayersToTrue()
          } else {
            selectedPlayers = selectedPlayers.filter(player => 
              player.player_number != playerNumber
            )
          }
        }

        const select = (value) => {
          for (let i = 0; i < playersCheckboxes.length; ++i){
            playersCheckboxes[i].checked = value
          }
        }

        const unSelectAllPlayers = () => {
          if (!isSelectAllPlayers.value) {
            select(false)
            selectedPlayers = []
          }
        }

        const addAllToSelectedPlayers = () => {
          for(const player in players.value) {
            selectedPlayers.push(players.value[player])
          }
        }

        const setSelectAllPlayersToTrue = () => {
          const numberOfPlayers = Object.keys(players.value).length
          const allIsSelected = selectedPlayers.length == numberOfPlayers
          isSelectAllPlayers.value = allIsSelected
        }

        const importPlayersAPICall = () => {
          if (selectedPlayers.length == 0) {
            errors.value['non_field_errors'] = ['Please select a player.']
            return 
          }
          isLoading.value = true
          const data = getData()
          const url = '/api/team/players/import/season-'
            + current_season.value
            + '/team-'
            + teamId.value
            + '/'
          
          axios
            .post(url, data)
            .then(response => {
              removeSelectedPlayers()
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        } 

        const getData = () => {
          const data = {
            'players': ''
          }
          let playerNumberField = ''
          let playerPositionField = ''
          
          for (let i = 0; i < selectedPlayers.length; ++i) {
            playerNumberField = `player-number-${selectedPlayers[i].id}`
            playerPositionField = `player-position-${selectedPlayers[i].id}`

            if (i == 0) {
              data.players += selectedPlayers[i].id
            } else {
              data.players += ',' + selectedPlayers[i].id
            }
            
            data[playerNumberField] = selectedPlayers[i].player_number
            data[playerPositionField]= selectedPlayers[i].position
          }

          return data
        }

        const removeSelectedPlayers = () => {
          for (let i = 0; i < selectedPlayers.length; ++i) {
            delete players.value[selectedPlayers[i].player_number]
          }

          selectedPlayers = []
        }
      /**
       * End of Methods
       */
      return {
        players,
        isSelectAllPlayers,
        errors,
        isLoading,
        importPlayer,
        unSelectAllPlayers,
        importPlayersAPICall
      }
    }
  }
</script>