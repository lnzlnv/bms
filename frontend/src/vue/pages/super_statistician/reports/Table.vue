<template>
  <div class="mb-[8rem]">
    <div class="mb-[2rem]">
    <img
      class="img-7 mx-[auto]"
      :src="team? team.logo:''"
      alt=""
    />
    </div>

    <form @submit.prevent="1 + 1">
      <div class="overflow-auto">
        <table class="table-2">
          <thead class="uppercase text-center">
            <tr>
              <th class="table-2__header" rowspan="2">No.</th>
              <th class="table-2__header lg" rowspan="2">Names</th>
              <th class="table-2__header bg-gray-2">PLAY</th>
              <th class="table-2__header lg" colspan="3">2 pts fg</th>
              <th class="table-2__header lg" colspan="3">3 pts fg</th>
              <th class="table-2__header lg" colspan="3">Total fg</th>
              <th class="table-2__header lg" colspan="3">Free Throw</th>
              <th class="table-2__header lg" colspan="3">Rebounds</th>
              <th class="table-2__header" rowspan="2">Assists</th>
              <th class="table-2__header" rowspan="2">Steals</th>
              <th class="table-2__header" rowspan="2">Blocks</th>
              <th class="table-2__header" rowspan="2">Turnovers</th>
              <th class="table-2__header" rowspan="2">Fouls</th>
              <th class="table-2__header" colspan="3">Total Shots</th>
              <th class="table-2__header" rowspan="2">Total Points</th>
            </tr>
            <tr>
              <th class="table-2__header bg-gray-2" rowspan="2">Min</th>
              <th class="table-2__header" rowspan="2">att</th>
              <th class="table-2__header" rowspan="2">made</th>
              <th class="table-2__header bg-gray-2" rowspan="2">%</th>
              <th class="table-2__header" rowspan="2">att</th>
              <th class="table-2__header" rowspan="2">made</th>
              <th class="table-2__header bg-gray-2" rowspan="2">%</th>
              <th class="table-2__header" rowspan="2">att</th>
              <th class="table-2__header" rowspan="2">made</th>
              <th class="table-2__header bg-gray-2" rowspan="2">%</th>
              <th class="table-2__header" rowspan="2">att</th>
              <th class="table-2__header" rowspan="2">made</th>
              <th class="table-2__header bg-gray-2" rowspan="2">%</th>
              <th class="table-2__header" rowspan="2">Off</th>
              <th class="table-2__header" rowspan="2">Def</th>
              <th class="table-2__header bg-gray-2" rowspan="2">total</th>
              <th class="table-2__header" rowspan="2">att</th>
              <th class="table-2__header" rowspan="2">made</th>
              <th class="table-2__header bg-gray-2" rowspan="2">%</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="player in team.players"
              :key="player.info.id"
              class="table-2__row"
            >
              <td 
                :class="updatedStats[player.info.player_number] ?
                  'active': ''"
                class="table-2__data text-center" 
                data-cell="Player Number">
                {{ player.info.player_number }}
              </td>
              <td
                :class="updatedStats[player.info.player_number] ?
                  'active': ''"
                class="table-2__data" 
                data-cell="Name"
              >
                {{ player.info.last_name }}
              </td>
              <td class="table-2__data" data-cell="Minutes Played">
                <Input
                  name="minutes"
                  :value="player.stats.minutes_played"
                  :statId="player.stats.id"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['two_pts_att'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="2 FG ATT"
                >
                <Input
                  name="two_pts_att"
                  :value="player.stats.two_pts_att"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['two_pts_made'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="2 FG Made"
              >
                <Input
                  name="two_pts_made"
                  :value="player.stats.two_pts_made"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td class="table-2__data bg-gray-2" data-cell="2 FG %">
                {{ computeTwoPtsPercentage(player.stats) }}
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['three_pts_att'] ?
                  'active' : ''
                "                class="table-2__data" 
                data-cell="3 fg att"
              >
                <Input
                  name="three_pts_att"
                  :value="player.stats.three_pts_att"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['three_pts_made'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="3 fg made"
              >
                <Input
                  name="three_pts_made"
                  :value="player.stats.three_pts_made"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td class="table-2__data bg-gray-2" data-cell="3 fg %">
                {{ computeThreePtsPercentage(player.stats) }}
              </td>
              <td class="table-2__data" data-cell="total shots att">
                {{ player.stats.two_pts_att + player.stats.three_pts_att }}
              </td>
              <td class="table-2__data" data-cell="total shots made">
                {{  player.stats.two_pts_made + player.stats.three_pts_made }}
              </td>
              <td class="table-2__data bg-gray-2" data-cell="total %">
                {{ computeTotalFGPercentage(player.stats)}}
                {{  }}
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['ft_att'] ?
                  'active' : ''
                "                
                class="table-2__data" data-cell="ft att"
              >
                <Input
                  name="ft_att"
                  :value="player.stats.ft_att"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['ft_made'] ?
                  'active' : ''
                "                
                class="table-2__data" 
                data-cell="ft made"
              >
                <Input
                  name="ft_made"
                  :value="player.stats.ft_made"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td class="table-2__data bg-gray-2" data-cell="ft %">
                {{ computeFTPercentage(player.stats) }}
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['reb_off'] ?
                  'active' : ''
                "                
                class="table-2__data" 
                data-cell="reb off"
              >
                <Input
                  name="reb_off"
                  :value="player.stats.reb_off"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['reb_def'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="reb def"
              >
                <Input
                  name="reb_def"
                  :value="player.stats.reb_def"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td class="table-2__data bg-gray-2" data-cell="reb total">
                {{ player.stats.reb_def + player.stats.reb_off }}
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['assists'] ?
                  'active' : ''
                "                
                class="table-2__data" 
                data-cell="assists"
              >
                <Input
                  name="assists"
                  :value="player.stats.assists"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['steals'] ?
                  'active' : ''
                "                
                class="table-2__data" 
                data-cell="steals"
              >
                <Input
                  name="steals"
                  :value="player.stats.steals"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['blocks'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="blocks"
              >
                <Input
                  name="blocks"
                  :value="player.stats.blocks"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['turnovers'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="turnovers"
              >
                <Input
                  name="turnovers"
                  :value="player.stats.turnovers"
                  :statId="player.stats.id"
                  :playerNumber="player.info.player_number"
                />
              </td>
              <td
                :class="
                  updatedStats[player.info.player_number] && 
                  updatedStats[player.info.player_number]['fouls'] ?
                  'active' : ''
                "
                class="table-2__data" 
                data-cell="fouls"
              >
                <span v-if="!isShowFoul">
                  <span
                    v-if="player.stats.is_ejected"
                    @click="showFoul"
                    class="ejected"
                  >
                    EJECTED
                  </span>
                  <span
                    v-else-if="player.stats.is_disqualified"
                    class="ejected"
                  >
                    DISQUALIFIED
                  </span>
                  <span
                    v-else-if="player.stats.fouls == 5"
                    class="ejected"
                  >
                    FO  
                  </span>
                  <span
                    v-else
                  >
                    <Input
                      name="fouls"
                      :value="player.stats.fouls"
                      :statId="player.stats.id"
                      :playerNumber="player.info.player_number"
                    />
                  </span>
                </span>

                <Input
                    v-if="isShowFoul"
                    name="fouls"
                    :value="player.stats.fouls"
                    :statId="player.stats.id"
                    :playerNumber="player.info.player_number"
                  />
              </td>
              <td class="table-2__data" data-cell="total shots att">
                {{ computeTotalShotsAtt(player.stats) }}
              </td>
              <td class="table-2__data" data-cell="total shots made">
                {{ computeTotalShotsMade(player.stats) }}
              </td>
              <td class="table-2__data bg-gray-2" data-cell="total shots %">
                {{ computeTotalShotsPercentage(player.stats) }}
              </td>
              <td class="table-2__data" data-cell="total points">
                {{ computeTotalPoints(player.stats) }}
              </td>
            </tr>
            <tr>
              <td class="table-2__data text-right label-1" colspan="3">
                Team Total
              </td>
              <td class="table-2__data" data-cell="2 fg att">
                {{ team.stats.two_pts_att }}
              </td>
              <td class="table-2__data" data-cell="2 fg made">
                {{ team.stats.two_pts_made }}
              </td>
              <td class="table-2__data bg-gray-2 label">
                {{ computeTwoPtsPercentage(team.stats) }}
              </td>
              <td class="table-2__data" data-cell="3 fg att">
                {{ team.stats.three_pts_att }}
              </td>
              <td class="table-2__data" data-cell="3 fg made">
                {{ team.stats.three_pts_made }}
              </td>
              <td class="table-2__data bg-gray-2 label">
                {{ computeThreePtsPercentage(team.stats) }}
              </td>
              <td class="table-2__data" data-cell="total att">
                {{ team.stats.two_pts_att + team.stats.three_pts_att }}
              </td>
              <td class="table-2__data" data-cell="total made">
                {{ team.stats.two_pts_made + team.stats.three_pts_made }}
              </td>
              <td class="table-2__data bg-gray-2 label">
                {{ team.stats.total_fg_percentage }}
              </td>
              <td class="table-2__data" data-cell="ft att">
                {{ team.stats.ft_att }}
              </td>
              <td class="table-2__data" data-cell="ft made">
                {{ team.stats.ft_made }}
              </td>
              <td class="table-2__data bg-gray-2 label">
                {{ computeFTPercentage(team.stats) }}
              </td>
              <td class="table-2__data" data-cell="reb off">
                {{ team.stats.reb_off }}
              </td>
              <td class="table-2__data" data-cell="reb def">
                {{ team.stats.reb_def }}
              </td>
              <td class="table-2__data bg-gray-2 label" data-cell="reb total">
                {{ team.stats.reb_off + team.stats.reb_def }}
              </td>
              <td class="table-2__data" data-cell="assists">
                {{ team.stats.assists }}
              </td>
              <td class="table-2__data" data-cell="steals">
                {{ team.stats.steals }}
              </td>
              <td class="table-2__data" data-cell="blocks">
                {{ team.stats.blocks }}
              </td>
              <td class="table-2__data" data-cell="turnovers">
                {{ team.stats.turnovers }}
              </td>
              <td class="table-2__data" data-cell="fouls">
                {{ team.stats.fouls }}
              </td>
              <td class="table-2__data" data-cell="total shots att">
                {{ computeTotalShotsAtt(team.stats) }}
              </td>
              <td class="table-2__data" data-cell="total shots made">
                {{ computeTotalShotsMade(team.stats) }}
              </td>
              <td class="table-2__data bg-gray-2 label">
                {{ computeTotalShotsPercentage(team.stats) }}
              </td>
              <td class="table-2__data" data-cell="total points">
                {{ computeTotalPoints(team.stats) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </form>
  </div>
</template>

<script>
  import axios from 'axios';
  import { inject, ref, watch } from 'vue';

  import Input from './Input.vue';

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

  export default {
    components: {
      Input
    },
    props: {
      team: {}
    },
    setup(props) {
      const isShowFoul = ref(false)
      const updatedPlayer = inject('updatedPlayer', updatedPlayer)
      const updatedStats = inject('updatedStats', updatedStats)

      /**
       * Methods
       */
        const showFoul = () => {
          isShowFoul.value = true
        }

        const computeTotalFGPercentage = (stats) => {
          const pointsMade = stats.two_pts_made + stats.three_pts_made
          if (pointsMade == 0) { return 0 }
          
          const pointsAtt = stats.two_pts_att + stats.three_pts_att
          return ((pointsMade / pointsAtt) * 100).toFixed(2)
        }

        const computeTwoPtsPercentage = (stats) => {
          if (stats.two_pts_made == 0) { return 0 }  
          return ((stats.two_pts_made /stats.two_pts_att)* 100).toFixed(2)
        }

        const computeTotalShotsAtt = (stats) => {
          return stats.two_pts_att + stats.three_pts_att + stats.ft_att
        }

        const computeTotalShotsMade = (stats) => {
          return stats.two_pts_made + stats.three_pts_made + stats.ft_made
        }

        const computeThreePtsPercentage = (stats) => {
          if (stats.three_pts_made == 0) { return 0 }
          return ((stats.three_pts_made / stats.three_pts_att) * 100).toFixed(2)
        }

        const computeTotalShotsPercentage = (stats) => {
          const shotsMade = computeTotalShotsMade(stats)
          if (shotsMade == 0) { return 0 }
          return ((shotsMade / computeTotalShotsAtt(stats)) * 100).toFixed(2)
        }

        const computeFTPercentage = (stats) => {
          if (stats.ft_made == 0) { return 0 }
          return ((stats.ft_made / stats.ft_att) * 100).toFixed(2)
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

      return {
        ...props,
        isShowFoul,
        updatedPlayer,
        updatedStats,
        showFoul,
        computeTotalFGPercentage,
        computeTotalShotsAtt,
        computeTotalShotsMade,
        computeTotalShotsPercentage,
        computeFTPercentage,
        computeTwoPtsPercentage,
        computeThreePtsPercentage,
        computeTotalPoints
      }
    }
  }
</script>