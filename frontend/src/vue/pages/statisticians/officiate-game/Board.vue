<template>
  <div v-if="game">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        An error occured! Please reload the page.
      </div>
    </div>
    
    <div 
      v-if="modalIsOpen"
      class="modal-1 flex justify-center items-center"
    >
      <div class="card-2">
        <p class="title-1 mb-[2rem]">
          End of the game. Game winner is {{ gameWinner }}.
        </p>

        <div class="text-center">
          <button 
            @click="modalIsOpen = false"
            class="btn-22"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>

    <SuccessMessage />

    <div class="lg:grid lg-grid-2-column-3 custom-h-full relative">
      <div>
        <ScoreBoard
          :game="game"
          :periods="periods"
        />
        <PlayerStats
          :game="game"
          :activeTeam="activeTeam"
          :inGameHomePlayers="inGameHomePlayers"
          :inGameAwayPlayers="inGameAwayPlayers"
        />
      </div>
      <div class="bg-1 p-[1em] min-h-full grid grid-2-rows-1 relative">
        <div 
          v-if="isLoading"
          class="loading-2 flex justify-center items-center"
        >
          <LoadingSpinner />
        </div>

        <div
          v-if="!hasGameWinner"
          class="mb-[1rem] flex justify-between items-center gap-[5px]"
        >
          <UndoRedo />

          <div class="flex">
            <input
              class="input-checkbox-1"
              type="checkbox"
              name=""
              id="substitution"
              hidden
              v-model="isForSubstitution"
              >
            <label class="btn-toggle" for="substitution"></label>
          </div>
        </div>
        <div v-if="!hasGameWinner">
          <div v-if="isForSubstitution">
            <SubstitutionBoard />
          </div>
          <div
            v-else
            class="grid grid-3-rows-1 h-full"
          >
            <PlayingPlayers
              :inGameHomePlayers="inGameHomePlayers"
              :inGameAwayPlayers="inGameAwayPlayers"
              :game="game"
              :activeTeam="activeTeam"
              :changeActiveTeam="changeActiveTeam"
            />
            <StatsButtons
              v-if="game.slug"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ScoreBoard from './ScoreBoard.vue';
  import PlayerStats from './PlayerStats.vue'
  import PlayingPlayers from './PlayingPlayers.vue'
  import StatsButtons from './StatsButtons.vue'
  import SuccessMessage from './SuccessMessage.vue'
  import { onBeforeMount, ref, provide, watch, reactive, computed } from 'vue';
  import SubstitutionBoard from './SubstitutionBoard.vue'
  import axios from 'axios';
  import setCsrfToken from '@composables/csrf-token.js';
  import normalize_data_2 from '@composables/normalize-data-2.js'
  import host from '@composables/host.js';
  import { error } from '@pages/admin/teams/create/composables.js'
  import { v4 as uuidv4 } from 'uuid';
  import UndoRedo from './UndoRedo.vue'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  setCsrfToken()
  
  export default {
    components: {
      ScoreBoard,
      PlayerStats,
      PlayingPlayers,
      StatsButtons,
      SuccessMessage,
      SubstitutionBoard,
      UndoRedo,
      LoadingSpinner
    },
    setup() {
      const gameId = ref(document.getElementById('js-game-id').value)
      const hasError = error()
      const roomMemberUniqueID = uuidv4() 
      const inGamePlayers = reactive({})
      const socket = ref(null)
      const hasGameWinner = ref(false)
      const gameWinner = ref(null)
      const game = ref({})
      const activeTeam = ref(null)
      const inGameHomePlayers = ref({})
      const inGameAwayPlayers = ref({})
      const periods = ref(0)
      const selectedPlayer = ref({})
      const messages = ref([])
      const messagesCount = ref(0)
      const isForSubstitution = ref(false)
      const substitution = reactive({
        homeTeam: {
          in: {},
          out: {}
        },
        awayTeam: {
          in: {},
          out: {}
        }
      })
      const isLoading = ref(false)
      const gameHasStarted = ref(false)
      const substitutionData = reactive({
        minutes: null,
        seconds: null,
        sub_in: null,
        sub_out: null
      })

      const modalIsOpen = ref(false);

      onBeforeMount(() => {
        isLoading.value = true
        const url = host + '/api/statistician/officiate-' + gameId.value + '/'

        axios
          .get(url)
          .then(response => {
            game.value = normalize_data_2(response.data)
            activeTeam.value = response.data.home_team.id
            periods.value = response.data.quarter
            hasGameWinner.value = response.data.has_game_winner
            setInGamePlayers(response.data)
            setSocketConnection()
            isLoading.value = false
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
          hasGameWinner,
          (hasWinner) => {
            if (hasWinner) {
              modalIsOpen.value = true
            }
          }
        )
        
        watch(
          hasGameWinner,
          (hasWinner) => {
            if (hasWinner) {
              const homeTeamWins = game.value.home_team.stats.total_points > game.value.away_team.stats.total_points
              if (homeTeamWins) {
                gameWinner.value = game.value.home_team.name
              } else {
                gameWinner.value = game.value.away_team.name
              }
            }
          } 
        )

        watch(
          inGamePlayers,
          (players) => {
            if (players == null) {
              return
            }

            addToInGame(
              inGameHomePlayers, 
              game.value.home_team.players, 
              players.home_team
            )

            addToInGame(
              inGameAwayPlayers, 
              game.value.away_team.players, 
              players.away_team
            )
          },
          {
            deep: true
          }
        )

        watch(
          messagesCount,
          (newCount, oldCount) => {
            if (newCount < oldCount) { return }

            setTimeout(() => {
                messages.value.shift()
                messagesCount.value -= 1
              }, 3000);
          },
          {
            deep: true
          }
        )
      /**
       * End of Watch
       */

      /**
       * Computed
       */
        const gameSlug = computed(() => {
          return game.value.slug
        })
      /**
       * End of Computed
       */

      /**
       * Methods
       */
        const setInGamePlayers = (data) => {
          if (!data.in_game_players) {
            inGamePlayers['home_team'] = []
            inGamePlayers['away_team'] = []
            return
          }

          inGamePlayers['home_team'] = data.in_game_players.home_team
          inGamePlayers['away_team'] = data.in_game_players.away_team
        }

        const setSocketConnection = () => {
          socket.value = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/officiate-game/'
            + game.value.slug
            + '/'
          )

          socket.value.onmessage = (event) => {
            let data = JSON.parse(event.data)

            if (data.operation && data.history) {
              data['content'] = data.history.content
            }

            updateUI(data)
            isLoading.value = false
          }

          socket.value.onclose = (event) => {
            console.error('Socket closed unexpectedly.')
            hasError.value = true
            isLoading.value = false
          }
        }

        const updateUI = (data) => {
          if (data.content == undefined) { return }

          const isHistory = data.type == 'history'
          const teamId = isHistory ? data.history.team_id : data.team_id

          const isHomeTeam = teamId == game.value.home_team.id
          const changeStatsHistory = isHistory && data.history.type == 'stats'
          
          if (data.type == 'stats' || changeStatsHistory) {
            const team = isHomeTeam ? 
              game.value.home_team : game.value.away_team
            const playerNumber = changeStatsHistory ? 
              data.history.player_number : data.player_number
            
              const player = isHomeTeam ? 
              team.players[playerNumber] 
                : team.players[playerNumber]

            if (player == undefined) { return }

            updatePoints(data, team, player)
            updateFouls(data, player)
            displaySuccessMessage(data)
          } else if (data.type == 'substitution') {
            inGamePlayers.home_team = data.players.home_team
            inGamePlayers.away_team = data.players.away_team
            displaySuccessMessage(data) 
          } else if (data.type == 'quarter') {
            periods.value = data.content.quarter
          } else if (data.type == 'game_winner') {
            hasGameWinner.value = true
          } else {
            // do nothing
          }
        }

        const displaySuccessMessage = (data) => {
          const isSender = roomMemberUniqueID == data.room_member_id
          if (isSender) {
              addSuccessMessage(data.message)
            }
        }

        const updatePoints = (data, team, player) => {
          if (data.content && data.content.points == undefined) { return }

          if (data.operation == 'REDO' || data.operation == undefined) {
            team.stats.total_points += data.content.points
            player.stats.total_points += data.content.points
            return
          }
          
          team.stats.total_points -= data.content.points
          player.stats.total_points -= data.content.points
        }

        const updateFouls = (data, player) => {
          if (data.content == undefined) { return }

          const isRedo = data.operation == 'REDO' || data.operation == undefined

          const isFoul = 'fouls' in data.content
          if (isFoul) {
            if (isRedo) {
              player.stats.fouls += data.content.fouls
            } else {
              player.stats.fouls -= data.content.fouls
            }
            return
          }

          const isEjected = 'ejected' in data.content
          if (isEjected) {
            player.stats.is_ejected = isRedo
            return
          }

          const isDisqualified = 'disqualified' in data.content
          if (isDisqualified) {
            player.stats.is_disqualified = isRedo
            return
          }
        }

        const addToInGame = (inGameStorage, players, inGame) => {
          const data = {}
          for (let i = 0; i < inGame.length; ++i) {
            data[inGame[i]] = players[inGame[i]]
          }
          inGameStorage.value = data
        }

        const changeActiveTeam = (id) => {
          activeTeam.value = id
          selectedPlayer.value = {}
        }

        const selectPlayer = (player) => {
          if (isForSubstitution.value) {
            return
          }
          selectedPlayer.value = player
        }

        const addSuccessMessage = (message) => {
          messages.value.push(message)
          messagesCount.value += 1;
        }
      /**
       * End of Methods
       */

      provide('substitutionData', substitutionData)
      provide('game', game)
      provide('inGameHomePlayers', inGameHomePlayers)
      provide('inGameAwayPlayers', inGameAwayPlayers)
      provide('activeTeam', activeTeam)
      provide('periods', periods)
      provide('substitution', substitution)
      provide('changeActiveTeam', changeActiveTeam)
      provide('selectPlayer', selectPlayer)
      provide('selectedPlayer', selectedPlayer)
      provide('addSuccessMessage', addSuccessMessage)
      provide('messages', messages)
      provide('isForSubstitution', isForSubstitution)
      provide('messages', messages)
      provide('messagesCount', messagesCount)
      provide('gameHasStarted', gameHasStarted)
      provide('hasGameWinner', hasGameWinner)
      provide('socket', socket)
      provide('roomMemberUniqueID', roomMemberUniqueID)
      provide('isLoading', isLoading)

      return {
        game,
        activeTeam,
        inGameHomePlayers,
        inGameAwayPlayers,
        periods,
        isForSubstitution,
        hasGameWinner,
        gameWinner,
        modalIsOpen,
        gameSlug,
        hasError,
        isLoading,
        changeActiveTeam,
      }
    }
  }
</script>