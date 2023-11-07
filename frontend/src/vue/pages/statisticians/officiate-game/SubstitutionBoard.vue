<template>
  <div class="substitution">
    <div>
      <PlayingPlayers
        :inGameHomePlayers="inGameHomePlayers"
        :inGameAwayPlayers="inGameAwayPlayers"
        :game="game"
        :activeTeam="activeTeam"
        :changeActiveTeam="changeActiveTeam"
      />
    </div>
    
    <SubstitutionForm />
  </div>
</template>

<script>
  import { inject } from 'vue';
  import PlayingPlayers from './PlayingPlayers.vue';
  import SubstitutionForm from './SubstitutionForm.vue'

  export default {
    components: {
      PlayingPlayers,
      SubstitutionForm
    },
    setup(props) {
      const inGameHomePlayers = inject('inGameHomePlayers', inGameHomePlayers)
      const inGameAwayPlayers = inject('inGameAwayPlayers', inGameAwayPlayers)
      const game = inject('game', game)
      const activeTeam = inject('activeTeam', activeTeam)
      const changeActiveTeam = inject('changeActiveTeam', changeActiveTeam)

      return {
        inGameHomePlayers,
        inGameAwayPlayers,
        game,
        activeTeam,
        changeActiveTeam,
      }
    }
  }
</script>