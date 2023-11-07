<template>
  <div class="grid grid-container-7 gap-[10px] mb-[1rem]">
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Steal' + message,
        class: 'success-2',
        data: {
          steals: 1
        }
      })"
    >
      Steal
    </button>
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Off Rebound' + message,
        class: 'success-2',
        data: {
          reb_off: 1
        }
      })"
    >
      Off Rebound
    </button>
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Def Rebound' + message,
        class: 'success-2',
        data: {
          reb_def: 1
        }
      })"
    >
      Def Rebound
    </button>
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Turnover' + message,
        class: 'success-2',
        data: {
          turnovers: 1
        }
      })"
    >
      Turnover
    </button>
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Assist' + message,
        class: 'success-2',
        data: {
          assists: 1
        }
      })"
    >
      Assist
    </button>
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Block' + message,
        class: 'success-2',
        data: {
          blocks: 1
        }
      })"
    >
      Block
    </button>
    <button 
      class="btn-15"
      @click="updateStats({
        content: 'Foul' + message,
        class: 'success-2',
        data: {
          fouls: 1
        }
      })"
    >
      Foul
    </button>
    <button 
      class="btn-17"
      @click="updateStats({
        content: 'Ejected' + message,
        class: 'delete-1',
        data: {
          ejected: true
        }
      })"
    >
      Ejected
    </button>
    <button 
      class="btn-17"
      @click="updateStats({
        content: 'Disqualified' + message,
        class: 'delete-1',
        data: {
          disqualified: true
        }
      })"
    >
      Disqualified
    </button>
  </div>

  <div class="grid grid-container-4 gap-[10px]">
    <div class="mb-[1rem] md:mb-0">
      <p class="player-stats__label">Off Turnover</p>
      <div class="grid gap-[10px] grid-3-rows-2 h-custom-2">
        <button 
          class="btn-16"
          @click="updateStats({
            content: 'Off Turnover 3PT Made' + message,
            class: 'success-1',
            data: {
              three_pts_made: 1,
              three_pts_att: 1,
              off_turnover: true,
              points: 3
            }
          })"
        >
          3PT Made
        </button>
        <button 
          class="btn-16"
          @click="updateStats({
            content: 'Off Turnover 2PT Made' + message,
            class: 'success-1',
            data: {
              two_pts_made: 1,
              two_pts_att: 1,
              off_turnover: true,
              points: 2
            }
          })"
        >
          2PT Made
        </button>
        <button 
            class="btn-16"
            @click="updateStats({
              content: 'Off Turnover FT Made' + message,
              class: 'success-1',
              data: {
                ft_att: 1,
                ft_made: 1,
                points: 1
              }
            })"
          >
            FT Made
          </button>
      </div>
    </div>

    <div class="mb-[1rem] md:mb-0">
      <p class="player-stats__label">Fast Break</p>
      <div class="grid gap-[10px] grid-3-rows-2 h-custom-2">
        <button 
          class="btn-16"
          @click="updateStats({
            content: 'Fast Break 3PT Made' + message,
            class: 'success-1',
            data: {
              three_pts_made: 1,
              three_pts_att: 1,
              fast_break: true,
              points: 3
            }
          })"
        >
          3PT Made
        </button>
        <button 
          class="btn-16"
          @click="updateStats({
            content: 'Fast Break 2PT Made' + message,
            class: 'success-1',
            data: {
              two_pts_made: 1,
              two_pts_att: 1,
              fast_break: true,
              points: 2
            }
          })"
        >
          2PT Made
        </button>
        <button 
            class="btn-16"
            @click="updateStats({
              content: 'Fast Break FT Made' + message,
              class: 'success-1',
              data: {
                ft_att: 1,
                ft_made: 1,
                points: 1
              }
            })"
          >
            FT Made
          </button>
      </div>
    </div>
    <div class="mb-[1rem] md:mb-0">
      <p class="player-stats__label">Second Chance</p>
      <div class="grid gap-[10px] grid-3-rows-2 h-custom-2">
        <button 
          class="btn-16"
          @click="updateStats({
            content: 'Second Chance 3PT Made' + message,
            class: 'success-1',
            data: {
              three_pts_made: 1,
              three_pts_att: 1,
              second_chance: true,
              points: 3
            }
          })"
        >
          3PT Made
        </button>
        <button 
          class="btn-16"
          @click="updateStats({
            content: 'Second Chance 2PT Made' + message,
            class: 'success-1',
            data: {
              two_pts_made: 1,
              two_pts_att: 1,
              second_chance: true,
              points: 2
            }
          })"
        >
          2PT Made
        </button>
        <button 
            class="btn-16"
            @click="updateStats({
              content: 'Second Chance FT Made' + message,
              class: 'success-1',
              data: {
                ft_att: 1,
                ft_made: 1,
                points: 1
              }
            })"
          >
            FT Made
          </button>
      </div>
    </div>
    <div class="mb-[1rem] md:mb-0">
      <p class="player-stats__label">Normal</p>
      <div class="grid gap-[10px] grid-3-rows-2 h-custom-2">
        <button 
          class="btn-16"
          @click="updateStats({
            content: '3PT Made' + message,
            class: 'success-1',
            data: {
              three_pts_made: 1,
              three_pts_att: 1,
              points: 3
            }
          })"
        >
          3PT Made
        </button>
        <button 
          class="btn-16"
          @click="updateStats({
            content: '2PT Made' + message,
            class: 'success-1',
            data: {
              two_pts_made: 1,
              two_pts_att: 1,
              points: 2
            }
          })"
        >
          2PT Made
        </button>
        <button 
            class="btn-16"
            @click="updateStats({
              content: 'FT Made' + message,
              class: 'success-1',
              data: {
                ft_att: 1,
                ft_made: 1,
                points: 1
              }
            })"
          >
            FT Made
          </button>
      </div>
    </div>
    <div>
      <p class="player-stats__label">Shots Miss</p>
      <div class="grid gap-[10px] grid-3-rows-2 h-custom-2">
          <button 
            class="btn-17"
            @click="updateStats({
              content: '3PT Miss' + message,
              class: 'delete-1',
              data: {
                three_pts_att: 1,
              }
            })"
          >
            3PT Miss
          </button>
          <button 
            class="btn-17"
            @click="updateStats({
              content: '2PT Miss' + message,
              class: 'delete-1',
              data: {
                two_pts_att: 1,
              }
            })"
          >
            2PT Miss
          </button>
          <button 
            class="btn-17"
            @click="updateStats({
              content: 'FT Miss' + message,
              class: 'delete-1',
              data: {
                ft_att: 1,
              }
            })"
          >
            FT Miss
          </button>
        </div>
    </div>
  </div>
</template>

<script>
  import { computed, inject, ref } from 'vue';
  import setCsrfToken from '@composables/csrf-token.js';

  setCsrfToken()

  export default {

    setup() {
      const message = ref(' successfully recorded!')
      const selectedPlayer = inject('selectedPlayer', selectedPlayer)
      const periods = inject('periods', periods)
      const inGameHomePlayers = inject('inGameHomePlayers', inGameHomePlayers)
      const inGameAwayPlayers = inject('inGameAwayPlayers', inGameAwayPlayers)
      const roomMemberUniqueID = inject('roomMemberUniqueID', roomMemberUniqueID)
      const isLoading = inject('isLoading', isLoading)
      const game = inject('game', game)
      const activeTeam = inject('activeTeam', activeTeam)
      const addSuccessMessage = inject('addSuccessMessage', addSuccessMessage)
      const messages = inject('messages', messages)
      const messagesCount = inject('messagesCount', messagesCount)
      const socket = inject('socket', socket)   

      const numberOfInGamePlayers = computed(() => {
        return Object.keys(inGameHomePlayers.value).length + Object.keys(inGameAwayPlayers.value).length
      })

      const updateStats = (message) => {
        const gameHasStarted = periods.value > 0

        if (!gameHasStarted) {
          messages.value.push({
            content: 'Period is 0. Cannot update stats.',
            class: 'delete-1'
          })
          messagesCount.value += 1;
          return
        }

        if (numberOfInGamePlayers.value != 10) {
          messages.value.push({
            content: 'Teams must have 5 in-game players each.',
            class: 'delete-1'
          })
          messagesCount.value += 1;
          return
        }

        const hasSelectedPlayer = displaySuccessMessage(message)
        

        if (!hasSelectedPlayer) {
          return
        }

        const isFouledOut = selectedPlayer.value.stats.fouls >= 5 || selectedPlayer.value.stats.is_ejected || selectedPlayer.value.stats.is_disqualified
        if (isFouledOut) {
          messages.value.push({
            content: 'Player is already fouled out or ejected.',
            class: 'delete-1'
          })
          messagesCount.value += 1;
          return
        }

        perform_update_stats(message)
      }

      const displaySuccessMessage = (message) => {
        const hasSelectedPlayer = Object.keys(selectedPlayer.value).length > 0
        
        if (!hasSelectedPlayer) {
          messages.value.push({
            content: 'Please select a player.',
            class: 'delete-1'
          })

          messagesCount.value += 1;
        } 

        return hasSelectedPlayer
      }

      const perform_update_stats = (message) => {
          if ('points' in message.data) {
            message.data['quarter'] = periods.value
          }
        
        const data = {
          content: message.data,
          type: 'stats',
          player_number: selectedPlayer.value.number,
          game_id: game.value.id,
          team_id: activeTeam.value,
          player_id: selectedPlayer.value.id,
          stat_id: selectedPlayer.value.stats.id,
          message: message,
          room_member_id: roomMemberUniqueID,
          statistician: game.value.statistician.id
        }
        isLoading.value = true
        socket.value.send(JSON.stringify(data))
      }

      return {
        updateStats,
        message
      }
    }
  }
</script>