<template>
  <div
    v-if="hasError"
    class="container-6 flex justify-center z-[1000000000000]"
  >
    <div class="delete-1">An error occured!</div>
  </div>

  <div class="container-2 flex justify-evenly overflow-hidden mb-[2.875rem]">
    <div v-for="team in teams" :key="team.id" class="px-[0.5em]">
      <img class="img-1 mx-0" :src="team.logo" />
    </div>
  </div>

  <div class="px-[1em] relative md:px-[2em] lg:px-[5.5em]">
    <div v-if="isLoading" class="loading-3 flex justify-center">
      <LoadingSpinner />
    </div>

    <div class="md:flex justify-between items-center">
      <div class="mb-[1rem]">
        <button
          @click="activeTab = 'ELIMINATIONS'"
          :class="activeTab == 'ELIMINATIONS' ? 'active' : ''"
          class="btn-21"
        >
          Eliminations
        </button>
        <button
          @click="activeTab = 'PLAYOFFS'"
          :class="activeTab == 'PLAYOFFS' ? 'active' : ''"
          class="btn-21"
        >
          Playoffs
        </button>
      </div>
      <form class="mb-[1rem] flex justify-end items-start gap-[20px]">
        <div>
          <select
            v-model="season"
            class="input-field-5"
            name="division"
            id="division"
          >
            <option value="" disabled selected>Select Season</option>
            <option
              v-for="season in options.seasons"
              :key="season.id"
              :value="season.id"
            >
              {{ season.year }}
            </option>
          </select>
        </div>
        <div>
          <select
            v-model="division"
            class="input-field-5"
            name="division"
            id="division"
          >
            <option value="" disabled selected>Select Division</option>
            <option value="J">Junior</option>
            <option value="S">Senior</option>
          </select>
        </div>
      </form>
    </div>

    <div class="overflow-x-auto">
      <table class="table-1 stats">
        <thead>
          <tr>
            <th class="table-1__header">RANK</th>
            <th class="table-1__header text-left lg">NAME</th>
            <th class="table-1__header">TEAM</th>
            <th class="table-1__header" title="Games Played">GP</th>
            <th class="table-1__header" title="Minutes Played">MP</th>
            <th class="table-1__header text-right" title="Points Per Game">
              PPG
            </th>
            <th class="table-1__header text-right" title="Field Goals Made">
              FGM
            </th>
            <th class="table-1__header text-right" title="Field Goals Attempt">
              FGA
            </th>
            <th
              class="table-1__header text-right"
              title="Field Goals Percentage"
            >
              FG%
            </th>
            <th class="table-1__header text-right" title="2 Points Made">
              2PM
            </th>
            <th class="table-1__header text-right" title="2 Points Attempt">
              2PA
            </th>
            <th class="table-1__header text-right" title="2 Points Percentage">
              2P%
            </th>
            <th class="table-1__header text-right" title="3 Points Made">
              3PM
            </th>
            <th class="table-1__header text-right" title="3 Points Attempt">
              3PA
            </th>
            <th class="table-1__header text-right" title="3 Points Percentage">
              3P%
            </th>
            <th class="table-1__header text-right" title="Free Throws Made">
              FTM
            </th>
            <th class="table-1__header text-right" title="Free Throws Attempt">
              FTA
            </th>
            <th
              class="table-1__header text-right"
              title="Free Throw Percentage"
            >
              FT%
            </th>
            <th class="table-1__header text-right" title="Offensive Rebounds">
              OREB
            </th>
            <th class="table-1__header text-right" title="Defensive Rebounds">
              DREB
            </th>
            <th class="table-1__header text-right" title="Total Rebounds">
              REB
            </th>
            <th class="table-1__header text-right" title="Assists">AST</th>
            <th class="table-1__header text-right" title="Turnovers">TO</th>
            <th class="table-1__header text-right" title="Steals">STL</th>
            <th class="table-1__header text-right" title="Blocks">BLK</th>
          </tr>
        </thead>
        <tbody v-if="players.length > 0">
          <tr
            v-for="(player, index) in players"
            :key="player.id"
            class="table-1__row flex flex-col lg:table-row"
          >
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="RANK"
            >
              {{ index + 1 + limit * pageNumber }}
            </td>
            <td
              class="table-1__data name--remove text-left grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="NAME"
            >
              <!-- <a :href="player.info_page"> -->
                {{
                  player.player_info.first_name +
                  " " +
                  player.player_info.last_name
                }}
              <!-- </a> -->
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="TEAM"
            >
              {{ player.team.name }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell lg-text-right"
              data-cell="GP"
            >
              {{ player.games_played == 0 ? '-' : player.games_played }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell lg-text-right"
              data-cell="MP"
            >
              {{ player.games_played == 0 ? '-' : player.minutes_played }}
            </td>
            <td
              class="table-1__data grid grid-2-column-3 gap-[10px] lg:table-cell lg-text-right"
              data-cell="PPG"
            >
              {{ player.games_played == 0 ? '-' : player.pts_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FGM"
            >
              {{ player.games_played == 0 ? '-' : player.field_goal_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FGA"
            >
              {{ player.games_played == 0 ? '-' : player.field_goals_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FG%"
            >
              {{ player.games_played == 0 ? '-' : player.stat.total_fg_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PM"
            >
              {{ player.games_played == 0 ? '-' : player.two_pts_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PA"
            >
              {{ player.games_played == 0 ? '-' : player.two_pts_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3P%"
            >
              {{ player.games_played == 0 ? '-' : player.games_played == 0 ? '-' : player.stat.two_pts_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PM"
            >
              {{ player.games_played == 0 ? '-' : player.three_pts_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3PA"
            >
              {{ player.games_played == 0 ? '-' : player.three_pts_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="3P%"
            >
              {{ player.games_played == 0 ? '-' : player.stat.three_pts_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FTM"
            >
              {{ player.games_played == 0 ? '-' : player.ft_made_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FTA"
            >
              {{ player.games_played == 0 ? '-' : player.ft_att_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="FT%"
            >
              {{ player.games_played == 0 ? '-' : player.stat.ft_percentage }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="OREB"
            >
              {{ player.games_played == 0 ? '-' : player.reb_off_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="DREB"
            >
              {{ player.games_played == 0 ? '-' : player.reb_def_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="REB"
            >
              {{ player.games_played == 0 ? '-' : player.reb_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="AST"
            >
              {{ player.games_played == 0 ? '-' : player.assists_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="TO"
            >
              {{ player.games_played == 0 ? '-' : player.turnovers_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="STL"
            >
              {{ player.games_played == 0 ? '-' : player.steals_per_game }}
            </td>
            <td
              class="table-1__data lg:text-right grid grid-2-column-3 gap-[10px] lg:table-cell"
              data-cell="STL"
            >
              {{ player.games_played == 0 ? '-' : player.blocks_per_game }}
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr class="table-1__row flex flex-col lg:table-row">
            <td
              class="table-1__data empty grid grid-2-column-3 gap-[10px] lg:table-cell"
              colspan="24"
            >
              No available stats.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-if="playersData.previous"
          @click="previous(playersUrl)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-if="playersData.next"
          @click="next(playersUrl)"
          class="btn-11"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onBeforeMount, ref, watch } from "vue";
import axios from "axios";
import LoadingSpinner from "@templates/LoadingSpinner.vue";
import { error } from "@pages/admin/teams/create/composables.js";
import { page } from "@pages/admin/teams/all/composables.js";

export default {
  name: "Table",
  components: {
    LoadingSpinner,
  },
  setup() {
    const allTeams = ref([]);
    const division = ref("J");
    const options = ref({});
    const season = ref("");
    const playersData = ref([]);
    const hasError = error();
    const activeTab = ref("ELIMINATIONS");
    const isLoading = ref(false);

    onBeforeMount(() => {
      const url = "/api/public/players/options/";

      axios
        .get(url)
        .then((response) => {
          options.value = response.data;
          season.value = response.data.current_season.id;
        })
        .catch((err) => {
          hasError.value = true;
        });

      const teamsUrl = "/api/teams/view/public/all/";

      isLoading.value = true;
      axios
        .get(teamsUrl)
        .then((response) => {
          allTeams.value = response.data;
          isLoading.value = false;
        })
        .catch((err) => {
          isLoading.value = false;
          hasError.value = true;
        });
    });

    /**
     * Computed
     */
    const teams = computed(() => {
      if (allTeams.value == undefined) {
        return;
      }
      return allTeams.value.filter((team) => team.division == division.value);
    });

    const playersUrl = computed(() => {
      return (
        "/api/public/standings/all/players/" +
        season.value +
        "/" +
        division.value +
        "/" +
        `?limit=${limit}&offset=${limit * pageNumber.value}` +
        `&standing_type=${activeTab.value}`
      );
    });

    const players = computed(() => {
      if (playersData.value.results == undefined) {
        return [];
      }

      return playersData.value.results.sort((a, b) => {
        return b.pts_per_game - a.pts_per_game;
      });
    });
    /**
     * End of Computed
     */

    /**
     * Watch
     */
    watch([season, division, activeTab], () => {
      pageNumber.value = 0;
      getPlayers(playersUrl.value);
    });
    /**
     * End of Watch
     */

    /**
     * Methods
     */
    const getPlayers = (url) => {
      isLoading.value = true;
      axios
        .get(url)
        .then((response) => {
          playersData.value = response.data;
          console.log(playersData.value);
          isLoading.value = false;
        })
        .catch((err) => {
          isLoading.value = false;
          hasError.value = true;
        });
    };
    /**
     * End of Methods
     */

    const { pageNumber, limit, next, previous } = page(getPlayers, 20);

    return {
      teams,
      division,
      options,
      season,
      hasError,
      players,
      playersData,
      pageNumber,
      limit,
      next,
      previous,
      playersUrl,
      activeTab,
      isLoading,
    };
  },
};
</script>
