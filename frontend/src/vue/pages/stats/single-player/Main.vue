<template>
  <div 
    v-if="isLoading"
    class="loading-3 flex justify-center"
  >
    <LoadingSpinner />
  </div>

  <div 
    v-if="hasError"
    class="container-6 flex justify-center z-[1000000000000]"
  >
    <div class="delete-1">
      An error occured!
    </div>
  </div>

  <div class="max-w-[1000px] mx-[auto] md:flex justify-between items-center mb-[1rem]">
    <div class="mb-[1rem] md:mb-0">
      <button
        @click="activeTab = 'ELIMINATIONS'"
        :class="activeTab == 'ELIMINATIONS' ? 'active': ''"
        class="btn-21"
      >
        Eliminations
      </button>
      <button
        @click="activeTab = 'PLAYOFFS'"
        :class="activeTab == 'PLAYOFFS' ? 'active': ''"
        class="btn-21"
      >
        Playoffs
      </button>
    </div>
    <form>
      <select
        class="input-field-1"
      >
        <option value="0" selected disabled>Select Season</option>
      </select>
    </form>
  </div>

  <div 
    v-if="Object.keys(stats).length > 0"
    class="player-info"
  >
    <div class="player-info__player grid items-end grid-3-column-1 gap-[10px] md:items-start">
      <img
        class="player-info__img"
        :src="samplePlayerPic"
        alt=""
      >

      <div class="md:hidden">
          <p class="player-info__name">
            {{ stats.player_info.fullname }}
          </p>
          <p class="leading-[20px]">
            {{ stats.player_info.position }}
            / 
            {{ stats.team.name }}
          </p>
          <p class="leading-[20px]">
            {{ stats.player_info.height }}
            / 
            {{ stats.player_info.weight }}
          </p>
      </div>

      <div class="hidden md:grid grid-2-column-3 gap-[20px] h-full">
        <div class="player-info__jersey-number">
          <div>5</div>
        </div>

        <div>
          <div class="md:flex flex-col justify-between h-full">
            <div class="md:grid grid-2-column-3 gap-[20px]">
              <div>
                <p class="player-info__name">
                </p>
                <p class="player-info__team">
                  / 
                </p>
              </div>
            </div>

            <div class="md:flex gap-[20px] z-[1000]">
              <div>
                <div class="player-info__stats-name">PPG</div>
                <div class="text-center font-[600]">
                  {{ stats.pts_per_game }}
                </div>
              </div>
        
              <div>
                <div class="player-info__stats-name">RPG</div>
                <div class="text-center font-[600]">
                  {{ stats.reb_per_game }}
                </div>
              </div>

              <div>
                <div class="player-info__stats-name">APG</div>
                <div class="text-center font-[600]">
                  {{ stats.assists_per_game }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <img
        class="player-info__team-logo md:hidden"
        src=""
        alt=""
      />

    </div>

    <div class="border-bottom-1 md:grid md-grid-2-column-4 md:mt-[1em]">
      <div class="flex flex-col justify-between">
        <div class="text-center p-[1em]">
          <h6 class="player-info__title">
            LEAGUE <br class="hidden md:block"> COMPARISON
          </h6>

          <p class="player-info__sub-title">Eliminations</p>
        </div>

        <div class="flex gap-[20px] justify-center md:grid md:justify-normal md-grid-2-column-2 md-bg-gray-1 md-border-right-1 md:pr-[0.5em]">
          <div class="flex items-center gap-[5px] md:min-h-[40px] justify-center">
            <div class="player-info__legend player"></div>
            <p class="player-info__legend-name">Player</p>
          </div>

          <div class="flex items-center gap-[5px] md:min-h-[40px] justify-center min-w-max">
            <div class="player-info__legend league"></div>
            <p class="player-info__legend-name">League Avg.</p>
          </div>
        </div>
      </div>

      <div class="">
        <div class="grid grid-5-column-1 items-end gap-[5px] px-[0.2em] min-h-[140px]">
          <div>
            <div class="grid grid-2-column-2 gap-[5px] items-end">
              <div>
                <p class="text-center font-[600]">
                  {{ stats.pts_per_game }}
                </p>
                <div 
                  class="player-info__bar player"
                  :style="`height: calc(140px * ${stats.ppg_percentage});`"
                ></div>
              </div>
        
              <!-- <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar league"></div>
              </div> -->
            </div>
          </div>
          <div>
            <div class="grid grid-2-column-2 gap-[5px] items-end">
              <div>
                <p class="text-center font-[600]">
                  {{ stats.reb_per_game }}
                </p>
                <div 
                  class="player-info__bar player"
                  :style="`height: calc(140px * ${stats.rpg_percentage});`"
                ></div>
              </div>
        
              <!-- <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar league"></div>
              </div> -->
            </div>
          </div>
          <div>
            <div class="grid grid-2-column-2 gap-[5px] items-end">
              <div>
                <p class="text-center font-[600]">
                  {{ stats.assists_per_game }}
                </p>
                <div 
                  class="player-info__bar player"
                  :style="`height: calc(140px * ${stats.apg_percentage});`"
                ></div>
              </div>
        
              <!-- <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar league"></div>
              </div> -->
            </div>
          </div>
          <div>
            <div class="grid grid-2-column-2 gap-[5px] items-end">
              <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar player"></div>
              </div>
        
              <!-- <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar league"></div>
              </div> -->
            </div>
          </div>
          <div>
            <div class="grid grid-2-column-2 gap-[5px] items-end">
              <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar player"></div>
              </div>
        
              <!-- <div>
                <p class="text-center font-[600]">9.2</p>
                <div class="player-info__bar league"></div>
              </div> -->
            </div>
          </div>
        </div>

        <div class="grid grid-5-column-1">
          <div class="player-info__bar-category">PPG</div>
          <div class="player-info__bar-category">RPG</div>
          <div class="player-info__bar-category">APG</div>
          <div class="player-info__bar-category">FT%</div>
          <div class="player-info__bar-category last">3P%</div>
        </div>
      </div>
    </div>

    <div id="root"></div>
  </div>
</template>

<script>
  import samplePlayerPic from '@images/sample-player-img.webp'
  import axios from 'axios';
  import { onBeforeMount, ref, watch } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import { error } from '@pages/admin/teams/create/composables.js'

  export default {
    components: {
      LoadingSpinner
    },
    setup() {
      const stats = ref({})
      const isLoading = ref(false)
      const hasError = error()
      const activeTab = ref('ELIMINATIONS')
      const season = ref(0)
      const options = ref({})
      let playerTeamId = ''

      onBeforeMount(() => {
        isLoading.value = true
        
        playerTeamId = document.getElementById('js-player-team-id').value
        const url = '/api/public/players/options'
        
        axios
          .get(url)
          .then(response => {
            options.value = response.data
            season.value = response.data.current_season.id
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      /**
       * Methods
       */
        const getPlayerStats = () => {
          isLoading.value = true

          
          const url = '/api/public/standings/single-player/'
            + playerTeamId
            + '/'
            +`?standing_type=${activeTab.value}`
            + `&season=${season.value}`

          axios
            .get(url)
            .then(response => {
              stats.value = response.data
              console.log(stats.value)
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true

            })
        }
      /**
       * End of Methods
       */

      watch(
        season,
        () => {
          getPlayerStats()
        }
      )

      return {
        samplePlayerPic,
        hasError,
        isLoading,
        activeTab,
        stats,
      }
    }
  }
</script>