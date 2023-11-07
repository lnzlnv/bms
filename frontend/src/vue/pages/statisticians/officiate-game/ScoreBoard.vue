<template>
  <div class="scoreboard">
    <div class="grid grid-2-column-2 gap-[20px] mb-[1rem]">
      <div v-if="game.home_team">
        <p class="scoreboard__label">
          {{ game.home_team.name }}
        </p>
        <div class="scoreboard__score">
          {{ game.home_team.stats.total_points }}
        </div>
      </div>
      <div v-if="game.away_team">
        <p class="scoreboard__label">
          {{ game.away_team.name }}
        </p>
        <div class="scoreboard__score">
          {{ game.away_team.stats.total_points }}
        </div>
      </div>
    </div>

    <div 
      class="min-h-[94.23px]"
    >
      <p class="scoreboard__label">Periods</p>
      <div class="scoreboard__periods grid grid-4-column-1">
        <button
          v-for="period in gamePeriods"
          :key="period"
          :class="period == periods ? 'active': ''"
          class="btn-13"
        >
          {{ period }}
        </button>
      </div>
    </div>
    <div v-if="periods > 4">
      <p class="scoreboard__label">OTS</p>
      <div class="scoreboard__periods grid grid-container-6">
        <button
          v-for="period in ots"
          :key="period"
          :class="period == ots ? 'active': ''"
          class="btn-13"
        >
          {{ period }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import { computed, inject, ref, watch } from 'vue';

  import setCsrfToken from '@composables/csrf-token.js';
  import host from '@composables/host.js';
import axios from 'axios';

  setCsrfToken()

  export default {
    props: {
      game: {},
      isForSubstitution: Boolean
    },
    setup(props) {
      const isForSubstitution = inject('isForSubstitution', isForSubstitution)
      const addSuccessMessage = inject('addSuccessMessage', addSuccessMessage)
      const periods = inject('periods', periods)
      const game = inject('game', game)
      const isLoading = inject('isLoading', isLoading)
      const inGameHomePlayers = inject('inGameHomePlayers', inGameHomePlayers)
      const inGameAwayPlayers = inject('inGameAwayPlayers', inGameAwayPlayers)
      const hasError = inject('hasError', hasError)

      const numberOfInGamePlayers = computed(() => {
        const inGameHomePlayerNumber = 
          Object.keys(inGameHomePlayers.value).length
        const inGameAwayPlayerNumber = 
          Object.keys(inGameAwayPlayers.value).length

          return inGameHomePlayerNumber 
          + inGameAwayPlayerNumber
      })

      const gameHasStarted = inject('gameHasStarted', gameHasStarted)
      const hasGameWinner = inject('hasGameWinner', hasGameWinner)

      const socket = inject('socket', socket)

      watch(
        numberOfInGamePlayers,
        (newValue, oldValue) => {
          const isStartOfAQuarter = newValue == 10 && oldValue == 5;
          if (isStartOfAQuarter) {
            gameHasStarted.value = true;
            addNewPeriod()
            return
          }

          const isEndOfAQuarter = newValue == 0 && oldValue == 10

          const endOfSecondQuarter = periods.value == 2
          
          if (isEndOfAQuarter && endOfSecondQuarter) {
            generateHalfTimeAnalysis()
          }

          if (isEndOfAQuarter) {
            const hasWinner = periods.value >= 4 
            && game.value.home_team.stats.total_points != game.value.away_team.stats.total_points
            
            if (hasWinner) {
              sendHasGameWinner()
              generateFullTimeAnalysis()
            }
          }
        }
      )

      const sendHasGameWinner = () => {
        const data = {
          type: 'game_winner',
        }
        isLoading.value = true
        socket.value.send(JSON.stringify(data))
      }

      const addNewPeriod = () => {
        const data = {
          type: 'quarter',
          content: {
            quarter: periods.value + 1
          },
          game_id: game.value.id,
          statistician: game.value.statistician.id
        }
        isLoading.value = true
        socket.value.send(JSON.stringify(data))
      }

      const messages = inject('messages', messages)

      const generateHalfTimeAnalysis = () => {
        isLoading.value = true
        const url = host + '/api/statistician/generate-analysis/2/' 
          + game.value.id + '/'

        axios
          .post(url)
          .then(response => {
            halfTimeAnalysisIsGenerated.value = true
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      }

      const halfTimeAnalysisIsGenerated = ref(false)
      const messagesCount = inject('messagesCount', messagesCount)

      watch(
        halfTimeAnalysisIsGenerated,
        (isGenerated) => {
          if (isGenerated) {
            messages.value.push({
              content: 'Half-Time Analysis is generated.',
              class: 'success-1'
            })
            messagesCount.value += 1
          }
        }
      )


      const generateFullTimeAnalysis = () => {
        isLoading.value = true
        const url = host + '/api/statistician/generate-analysis/' 
          + periods.value + '/' 
          + game.value.id + '/'

        axios
          .post(url)
          .then(response => {
            fullTimeAnalysisIsGenerated.value = true
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      }

      const fullTimeAnalysisIsGenerated = ref(false)

      watch(
        fullTimeAnalysisIsGenerated,
        (isGenerated) => {
          if (isGenerated) {
            messages.value.push({
              content: 'Full-Time Analysis is generated.',
              class: 'success-1'
            })
            messagesCount.value += 1
          }
        }
      )

      const substitution = inject('substitution', substitution)

      const gamePeriods = computed(() => {
        if (periods.value <= 4) {
          return periods.value
        }
        return 4
      })

      const ots = computed(() => {
        const ot = periods.value - 4
        if ( ot > 0) {
          return ot
        }
        return 0
      })

      const substitutionData = inject('substitutionData', substitutionData)

      return {
        ...props,
        gamePeriods,
        ots,
        isForSubstitution,
        addNewPeriod,
        periods
      }
    }
  }
</script>