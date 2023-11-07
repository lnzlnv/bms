<template>
  <div v-if="game" class="mx-[2em]">
    <div class="pos-item-4">
      <SuccessMessage />
    </div>

    <div 
      v-if="isApproved"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Game stats has been successfully approved!
      </div>
    </div>

    <div class="mb-[1rem]">
      <img 
        class="img-9 mx-auto"
        :src="game.season ? game.season.logo:''" 
        alt=""
      />
    </div>

    <div class="text-center mb-[2rem]">
      <button
        @click="approveGameStats"
        v-if="!game.is_approved_by_super_statistician && game.has_full_time_analysis && game.has_half_time_analysis"
        class="btn-22"
      >
        Approve Stats
      </button>

      <div>
        <div 
          v-if="game.is_approved_by_super_statistician"
          class="text-center title-2"
        > 
          <p>Approved by Lead Statistician:</p>
          <p>
            {{ game.approved_by_super_statistician.first_name }}
            {{ game.approved_by_super_statistician.last_name }}
          </p>
        </div>
      </div>
    </div>

    <TabButtons />
    <TabDropdown />

    <div class="overflow-hidden">
      <div v-show="activeTab == 1">
        <div v-if="!game.player_stats_are_generated">
          <h1 class="title-3">Game stats will be generated if the game is officiated.</h1>
        </div>

        <StatsReport
          v-if="game.player_stats_are_generated"
          :team="game.home_team"
          :totalPoints="computeTotalPoints(game.home_team.stats)"
        />
      </div>

      <div v-show="activeTab == 2">
        <div v-if="!game.player_stats_are_generated">
          <h1 class="title-3">Game stats will be generated if the game is officiated.</h1>
        </div>

        <StatsReport
          v-if="game.player_stats_are_generated"
          :team="game.away_team"
          :totalPoints="computeTotalPoints(game.away_team.stats)"
        />
      </div>

      <HalfTimeAnalysis 
        v-show="activeTab == 3"
        :game="game"
      />

      <FullTimeAnalysis 
        v-show="activeTab == 4"
        :game="game"
      />
    </div>
  </div>
</template>

<script>
  import { computed, onBeforeMount, provide, ref, watch } from 'vue';

  import TabButtons from './TabButtons.vue';
  import TabDropdown from './TabDropdown.vue';
  import StatsReport from './StatsReport.vue';
  import Analysis from './Analysis.vue'
  import HalfTimeAnalysis from './HalfTimeAnalysis.vue';
  import FullTimeAnalysis from './FullTimeAnalysis.vue';
  import SuccessMessage from '@pages/statisticians/officiate-game/SuccessMessage.vue'
  import normalizeData from '@composables/normalize-team-players-data.js'


  import host from '@composables/host.js';
  import axios from 'axios';

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    components: {
      TabButtons,
      TabDropdown,
      StatsReport,
      Analysis,
      HalfTimeAnalysis,
      FullTimeAnalysis,
      SuccessMessage
    },
    setup() {
      const game = ref(null)
      const activeTab = ref(1)
      const isApproved = ref(false)
      const isUpdated = ref(false)
      const messages = ref([])
      const messagesCount = ref(0)
      const socket = ref(null)
      const updatedPlayer = ref([])
      const updatedStats = ref({})
      const updatedPlayerCount = ref(0)
      const statsContent = ref({})

      onBeforeMount(() => {
        const gameId = document.getElementById('js-game-id').value
        const url = host + '/api/games-stats-approval/' + gameId + '/'

        axios
          .get(url)
          .then(response => {
            game.value = normalizeData(response.data)
            setSocketConnection()
          })
          .catch(err => {
            console.log(err)
          })
      })

      /**
       * Watch
       */
        watch(
          isApproved,
          (approved) => {
            if (!approved) {
              return
            }
            
            setTimeout(() => {
              isApproved.value = false
            }, 5000)
          }
        )

        watch(
          isUpdated,
          (updated) => {
            if (updated) {
              messages.value.push({
                content: 'Stat is updated successfully!',
                class: 'success-1'
              })
              messagesCount.value += 1
              isUpdated.value = false
            }
          }
        )

        watch(
          messagesCount,
          (newValue, oldValue) => {
            if (newValue > oldValue) {
              setTimeout(() => {
                messages.value.shift()
                messagesCount.value -= 1
              }, 5000)
            }
          }
        )

        watch(
          updatedPlayerCount,
          (newVal, oldVal) => {
            if (newVal > oldVal) {
              setTimeout(() => {
                delete updatedStats.value[updatedPlayer.value[0]]
                updatedPlayer.value.shift()
                updatedPlayerCount.value -= 1
                statsContent.value = {}
              }, 5000)
            }
          }
        )
      /**
       * End of Watch
       */

      /**
       * Computed
       */
        const activeTeam = computed(() => {
          if (activeTab.value == 1) {
            return game.value.home_team
          }

          if (activeTab.value == 2) {
            return game.value.away_team
          }

          return {
            stats: {
              id: 0
            }
          }
        })
      /**
       * End of Computed
       */


      /**
       * Methods
       */
        const setSocketConnection = () => {
          socket.value = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/officiate-game/'
            + game.value.slug
            + '/'
          )

          socket.value.onmessage = (event) => {
            const data = JSON.parse(event.data)
            const isHistory = data.type == 'history'
            const teamId = isHistory ? data.history.team_id : data.team_id
            const isHomeTeam = teamId == game.value.home_team.id

            if (teamId == undefined) { return }
            
            if (data.type == 'stats' || data.history.type == 'stats') {
              const team = isHomeTeam ? 
                game.value.home_team : game.value.away_team
              const playerNumber = isHistory ? 
                data.history.player_number : data.player_number
              const player = isHomeTeam ? 
                team.players[playerNumber] 
                  : team.players[playerNumber]

              if (player == undefined) { return }

              const newData = isHistory ? data.history : data
              const operation = 
                data.operation != undefined ? data.operation : 'REDO'

              updatePoints(newData, player, team, operation, playerNumber)
              updateFouls(newData, team, player, operation)
            }
          }

          socket.value.onclose = (event) => {
            console.error('Socket closed unexpectedly.')
          }
        }

        const updatePoints = (data, player, team, operation, playerNumber) => {
          updatedStats.value[playerNumber] = {}

          for (const key in data.content) {
            updatedStats.value[playerNumber][key] = key

            if (player.stats[key] != undefined) { 
              if (operation == 'REDO') {
                player.stats[key] += data.content[key]
                team.stats[key] += data.content[key]
              } else {
                player.stats[key] -= data.content[key]
                team.stats[key] -= data.content[key]
              }
            }
            
            if (team.points_classification[key] != undefined) {
              if (operation == 'REDO') {
                team.points_classification[key] += data.content.points
              } else {
                team.points_classification[key] -= data.content.points
              }
            }
          }
          updatedPlayer.value.push(playerNumber)
          updatedPlayerCount.value += 1
        }

        const updateFouls = (
          data, 
          team, 
          player,
          operation, 
        ) => {
          console.log(data.content)
          if (data.content == undefined) { return }
          
          if ('ejected' in data.content ) {
            if (operation == 'REDO') {
              player.stats.is_ejected = true
              team.stats.fouls -= player.stats.fouls
            } else {
              player.stats.is_ejected = false
              team.stats.fouls += player.stats.fouls
            }
          }

          if ('disqualified' in data.content ) {
            if (operation == 'REDO') {
              player.stats.is_disqualified = true
              team.stats.fouls -= player.stats.fouls
            } else {
              player.stats.is_disqualified = false
              team.stats.fouls += player.stats.fouls
            }
          }
        }

        const changeActiveTab = (tabNumber) => {
          activeTab.value = tabNumber
        }

        const approveGameStats = () => {
          const url = host + '/api/games-stats-approval/approve/' 
            + game.value.id + '/'

          axios
            .post(url)
            .then(response => {
              isApproved.value = true
              game.value.is_approved_by_super_statistician = true
            })
            .catch(err => {
              console.log(err)
            })
        }

        const updateStatType = (event, previousValue, classificationId, type) => {
          if (Number(event.target.value) == previousValue) { return }

          const data = {} 
          data[event.target.name] = event.target.value 
          
          const url = host + '/api/games-stats-approval/' 
            + type + '/' 
            + classificationId + '/'

          axios
            .patch(url, data)
            .then(response => {
              isUpdated.value = true
            })
            .catch(err => {
              console.log(err)
            })
        }

        const updateStat = (event, previousValue, statId, playerNumber) => {
          const newValue = Number(event.target.value) 

          if (newValue == previousValue) { return }
          
          const data = {} 
          const fieldName = event.target.name
          data[fieldName] = newValue

          const url = '/api/games-stats-approval/' 
            + 'team-stat-'
            + activeTeam.value.stats.id
            + '/'
            + statId 
            + '/'

          axios
            .patch(url, data)
            .then(response => {
              isUpdated.value = true
              updateTeamStat(previousValue, newValue, fieldName)
              activeTeam.value.players[playerNumber]['stats'][fieldName] = newValue
            })
            .catch(err => {
              console.log(err)
            })
        }

        const updateTeamStat = (previousValue, newValue, fieldName) => {
          if (activeTeam.value.stats.id <= 0) { return }

          const valueToBeAdded = newValue - previousValue
          activeTeam.value.stats[fieldName]  += valueToBeAdded
        }

        const computeTotalPoints = (stats) => {
          const twoPts = stats.two_pts_made * 2
          const threePts = stats.three_pts_made * 3
          const ftPts = stats.ft_made
          return twoPts + threePts + ftPts
        }
      /**
       * End of Methods
       */

      provide('activeTab', activeTab)
      provide('game', game)
      provide('changeActiveTab', changeActiveTab)
      provide('isUpdated', isUpdated)
      provide('messages', messages)
      provide('messagesCount', messagesCount)
      provide('updateStatType', updateStatType)
      provide('updateStat', updateStat)
      provide('updatedPlayer', updatedPlayer)
      provide('updatedStats', updatedStats)
      provide('statsContent', statsContent)

      return {
        activeTab,
        game,
        isApproved,
        changeActiveTab,
        approveGameStats,
        computeTotalPoints
      }
    }
  }
</script>