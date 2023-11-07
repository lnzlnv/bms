<template>
  <div 
      v-if="activeTeam == team.id"
      class="player-stats__team"
    >
    <p class="player-stats__label-3">{{ team.name }}</p>

    <div class="player-stats__players"> 
      <div v-for="player in team.players" :key="player.id">
        <div class="grid grid-2-column-4 mb-[0.2rem]">
          <div class="flex gap-[10px]">
            <div class="min-w-[24.45px]">
              <div v-if="(player.stats.fouls <= 4 || inGamePlayers[player.number] != null) && !(player.stats.is_ejected || player.stats.is_disqualified)">
                <button
                  v-if="((substitution.in[player.number] == null && inGamePlayers[player.number] == null)) && isForSubstitution"
                  @click="updateSubstitution(player, 'in')"
                  class="btn-18"
                >
                  +
                </button>
                <button
                  v-if="((substitution.in[player.number] != null) && substitution.out[player.number] == null) && isForSubstitution"
                  @click="updateSubstitution(player, 'out')"
                  class="btn-19"
                >
                  -
                </button>

                <button
                  v-if="(inGamePlayers[player.number] != null && substitution.out[player.number] == null) && isForSubstitution"
                  @click="updateSubstitution(player, 'out')"
                  class="btn-20"
                > 
                  i
                </button>

                <button
                  v-if="(inGamePlayers[player.number] != null && substitution.out[player.number] != null) && isForSubstitution"
                  @click="updateSubstitution(player, 'in')"
                  class="btn-19"
                > 
                  o
                </button>
              </div>
            </div>
            <p>{{ player.number }}</p>
            <p>{{ player.name }}</p>
          </div>

          <div class="grid grid-2-column-2 gap-[15px] text-center">
            <p
              :class="player.stats != null && (player.stats.is_ejected || player.stats.is_disqualified || player.stats.fouls >= 5) ?'ejected' : ''"
            >
              {{ player.stats == null ? 0 : 
                player.stats.is_ejected ? 'E':
                player.stats.is_disqualified ? 'D':
                player.stats.fouls == 5 ? 'FO': player.stats.fouls }}
            </p>
            <p>
              {{ player.stats == null ? 0 : player.stats.total_points }}
            </p>
          </div>
      </div>
    </div>
      </div>
  </div>
</template>

<script>
import { inject } from 'vue';

  export default {
    props: {
      team: {},
      activeTeam: Number,
      inGamePlayers: {},
      substitution: {}
    },
    setup(props) {
      const isForSubstitution = inject('isForSubstitution', isForSubstitution)
      const selectedPlayer = inject('selectedPlayer', selectedPlayer)
      const game = inject('game', game)

      const updateSubstitution = (player, status) => {
        if (status != 'in') {
          if (props.inGamePlayers[player.number] != null) {
            props.substitution.out[player.number] = player
          }
          
          delete props.substitution.in[player.number]
          
          return
        } 

        const numberOfInGamePlayers = Object.keys(props.inGamePlayers).length
        const inPlayers = Object.keys(props.substitution.in).length
        const outPlayers = Object.keys(props.substitution.out).length
        const playersNumber = (inPlayers + numberOfInGamePlayers) - outPlayers
        
        if (playersNumber == 5 && props.inGamePlayers[player.number] == null) {
          return
        }
        
        if ( props.inGamePlayers[player.number] == null) {
          props.substitution.in[player.number] = player
        }
        
        delete props.substitution.out[player.number]
      }

      const updateInGamePlayers = (id, players, operation, inGamePlayers) => {
        const alreadyFivePlayersInGame = Object.keys(inGamePlayers).length >=5
        
        const addPlayer = operation == '+'
        
        if ( addPlayer &&  alreadyFivePlayersInGame) {
          return
        }

        if (addPlayer) {
          for (let i = 0; i < players.length; ++i) {
            if (players[i].id == id) {
              inGamePlayers[id] = players[i]
              break
            }
          }
        }
        const isEmpty = Object.keys(inGamePlayers).length <= 0
        const removePlayer = operation == '-'

        if (removePlayer && isEmpty) {
          return
        }

        if (removePlayer) {
          delete inGamePlayers[id]
          if (selectedPlayer.value.id == id) {
            selectedPlayer.value = {}
          }
        }
      }

      return {
        ...props,
        isForSubstitution,
        updateSubstitution,
        updateInGamePlayers
      }
    }
  }
</script>