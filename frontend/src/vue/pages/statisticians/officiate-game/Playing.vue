<template>
  <div class="playing-players__team grid md-grid-2-column-4 gap-[10px]">
    <button 
      @click="changeActiveTeam(team.id)"
      :class="activeTeam == team.id? 'active' : ''"
      class="btn-14 team md:min-w-[300px]"
    >
      {{ team.name }}
    </button>

    <div 
      v-if="activeTeam == team.id"
      class="md:grid grid-container-5 gap-[10px]"
    >
      <button
        v-for="player in players"
        :key="player.id"
        class="btn-14 player mb-[1rem] md:mb-0"
        :class="player.id == selectedPlayer.id ? 'active' : ''"
        @click="selectPlayer(player)"
      >
        {{ player.number }}
      </button>
    </div>
  </div>
</template>

<script>
import { inject } from 'vue';

  export default {
    props: {
      team: {},
      players: {},
      activeTeam: Number,
      changeActiveTeam: Function,
    },
    setup(props) {
      const selectPlayer = inject('selectPlayer', selectPlayer)
      const selectedPlayer = inject('selectedPlayer', selectedPlayer)
      return {
        ...props,
        selectPlayer,
        selectedPlayer
      }
    } 
  }
</script>