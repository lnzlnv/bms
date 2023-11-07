<template>
  <div class="hidden md:block text-center mb-[2rem]">
    <button 
      @click="changeActiveTab(1)"
      :class="activeTab == 1 ? 'active':''"
      class="btn-21"
    >
      {{ game.home_team ? game.home_team.name : '' }}
    </button>
    <button 
      @click="changeActiveTab(2)"
      :class="activeTab == 2 ? 'active':''"
      class="btn-21"
    >
      {{ game.away_team ? game.away_team.name : '' }}
    </button>
    <button 
      @click="changeActiveTab(3)"
      :class="activeTab == 3 ? 'active':''"
      class="btn-21"
    >
      Half-Time Analysis
    </button>
    <button 
      @click="changeActiveTab(4)"
      :class="activeTab == 4 ? 'active':''"
      class="btn-21 full"
    >
      Full-Time Analysis
    </button>
  </div>
</template>

<script>
import { inject } from 'vue';

  export default {
    setup() {
      const activeTab = inject('activeTab', activeTab)
      const changeActiveTab = inject('changeActiveTab', changeActiveTab)
      
      const game = inject('game', game)

      return {
        activeTab,
        changeActiveTab,
        game
      }
    }
  }
</script>