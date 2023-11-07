<template>
  <div class="playing-players mb-[1rem]">
      <Playing 
        class="mb-[1rem]"
        v-if="game.home_team != null"
        :team="game.home_team"
        :players="inGameHomePlayers"
        :activeTeam="activeTeam"
        :changeActiveTeam="changeActiveTeam"
      />

      <Playing 
        v-if="game.away_team != null"
        :team="game.away_team"
        :players="inGameAwayPlayers"
        :activeTeam="activeTeam"
        :changeActiveTeam="changeActiveTeam"
      />
  </div>
</template>

<script>
  import Playing from './Playing.vue';

  export default {
    components: {
      Playing
    },
    props: {
      inGameHomePlayers: {},
      inGameAwayPlayers: {},
      game: {},
      activeTeam: Number,
      changeActiveTeam: Function,
      updateInGameHomePlayers: Function
    },
    setup(props) {
      return {
        ...props
      }
    }
  }
</script>