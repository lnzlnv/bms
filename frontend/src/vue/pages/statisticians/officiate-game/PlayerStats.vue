<template>
  <div class="player-stats">
    <div class="player-stats__header grid grid-2-column-4 items-center gap-[10px]">
      <p class="player-stats__label">Player Stats</p>

      <div class="grid grid-2-column-2 gap-[15px]">
        <p class="player-stats__label-2">Fouls</p>
        <p class="player-stats__label-2">Points</p>
      </div>
    </div>

    <PlayerList 
      v-if="game.home_team != null"
      :team="game.home_team"
      :activeTeam="activeTeam"
      :inGamePlayers="inGameHomePlayers"
      :substitution="substitution.homeTeam"
    />

    <PlayerList 
      v-if="game.away_team != null"
      :team="game.away_team"
      :activeTeam="activeTeam"
      :inGamePlayers="inGameAwayPlayers"
      :substitution="substitution.awayTeam"
    />
  </div>
</template>

<script>
  import { inject, onBeforeMount } from 'vue';
import PlayerList from './PlayerList.vue'

  export default {
    components: {
      PlayerList
    },
    props: {
      game: {},
      activeTeam: Number,
      inGameHomePlayers: {},
      inGameAwayPlayers: {}
    },
    setup(props) {
      const substitution = inject('substitution', substitution)

      return {
        ...props,
        substitution
      }
    }
  }
</script>