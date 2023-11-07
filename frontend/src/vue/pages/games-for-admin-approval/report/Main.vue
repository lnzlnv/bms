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

    <div>
      <img 
        class="img-9 mx-auto"
        :src="game.season ? game.season.logo:''" 
        alt=""
      />
    </div>

    <Approvals 
      :game="game"
    />

    <div>
      <TabButtons />
      <TabDropdown />
    </div>

    <div class="overflow-hidden">
      <div v-show="activeTab == 1">
        <div v-if="!game.player_stats_are_generated">
          <h1 class="title-3">Game stats will be generated if the game is officiated.</h1>
        </div>

        <StatsReport
          :team="game.home_team"
          :totalPoints="game.home_team.stats.total_points"
        />
      </div>

      <div v-show="activeTab == 2">
        <div v-if="!game.player_stats_are_generated">
          <h1 class="title-3">Game stats will be generated if the game is officiated.</h1>
        </div>

        <StatsReport
          :team="game.away_team"
          :totalPoints="game.away_team.stats.total_points"
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
  import axios from 'axios'
  import { onBeforeMount, provide, ref, watch } from 'vue'

  import host from '@composables/host.js';

  import TabButtons from '@pages/super_statistician/reports/TabButtons.vue';
  import TabDropdown from '@pages/super_statistician/reports/TabDropdown.vue';
  import StatsReport from '@pages/super_statistician/reports/StatsReport.vue';
  import HalfTimeAnalysis from '@pages/super_statistician/reports/HalfTimeAnalysis.vue';
  import FullTimeAnalysis from '@pages/super_statistician/reports/FullTimeAnalysis.vue';
  import Approvals from './Approvals.vue';

  import SuccessMessage from '@pages/statisticians/officiate-game/SuccessMessage.vue'

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    components: {
      TabButtons,
      TabDropdown,
      Approvals,
      StatsReport,
      HalfTimeAnalysis,
      FullTimeAnalysis,
      SuccessMessage
    },
    setup() {
      const game = ref(null)
      const updatedStats = ref({})
      const activeTab = ref(1)
      const isUpdated = ref(false)
      const messages = ref([])
      const messagesCount = ref(0)
      const statsContent = ref({})

      onBeforeMount(() => {
        const gameId = document.getElementById('js-game-id').value
        const url = host + '/api/games-stats-approval/' + gameId + '/'

        axios
          .get(url)
          .then(response => {
            game.value = response.data
          })
          .catch(err => {
            console.log(err)
          })
      })

      const changeActiveTab = (tabNumber) => {
        activeTab.value = tabNumber
      }

      const isApproved = ref(false)

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
          })
      }

      const updateStat = (event, previousValue, statId) => {
        if (Number(event.target.value) == previousValue) { return }
        
        const data = {} 
        data[event.target.name] = event.target.value 
        
        const url = host + '/api/games-stats-approval/' + statId + '/'

        axios
          .patch(url, data)
          .then(response => {
            isUpdated.value = true
          })
          .catch(err => {
            console.log(err)
          })
      }

      provide('game', game)
      provide('activeTab', activeTab)
      provide('changeActiveTab', changeActiveTab)
      provide('isApproved', isApproved)
      provide('messages', messages)
      provide('messagesCount', messagesCount)
      provide('updateStatType', updateStatType)
      provide('updateStat', updateStat)
      provide('updatedStats', updatedStats)
      provide('statsContent', statsContent)
      
      return {
        game,
        activeTab,
        isApproved
      }
    }
  }
</script>