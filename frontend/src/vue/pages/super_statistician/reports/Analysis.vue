<template>
  <div>
    <div class="mb-[5rem]">
      <h1 class="title-1">Bicol Universities and Colleges Athletic League</h1>
      <h5 class="title-2">Season {{ game.season ? game.season.year :'' }}</h5>
    </div>

    <h3 class="title-3 mb-[4rem]">{{ name }}</h3>

    <table class="table-4">
      <thead>
        <tr>
          <th class="table-4__header">
            {{ game.home_team.name }}
          </th>
          <th class="table-4__header">
            Team Name
          </th>
          <th class="table-4__header">
            {{ game.away_team.name }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="table-4__data">
            <div class="flex flex-col items-center md:block">
              <Input 
                name="two_pts_made"
                :value="homeStats.two_pts_made"
                :statId="homeStats.id"
              />
              /
              <Input 
                name="two_pts_att"
                :value="homeStats.two_pts_att"
                :statId="homeStats.id"
              />
            </div>
          </td>
          <td class="table-4__data">
            2 Points
          </td>
          <td class="table-4__data">
            <div class="flex flex-col items-center md:block">
              <Input
                name="two_pts_made"
                :value="awayStats.two_pts_made"
                :statId="awayStats.id"
              />
              /
              <Input
                name="two_pts_att"
                :value="awayStats.two_pts_att"
                :statId="awayStats.id"
              />
            </div>
          </td>
        </tr>

        <AnalysisTableRow 
          :col1="homeStats.two_pts_percentage"
          col2="%"
          :col3="awayStats.two_pts_percentage"
        />
        
        <tr>
          <td class="table-4__data">
            <div class="flex flex-col items-center md:block">
              <Input
                name="three_pts_made"
                :value="homeStats.three_pts_made"
                :statId="homeStats.id"
              />
              /
              <Input
                name="three_pts_att"
                :value="homeStats.three_pts_att"
                :statId="homeStats.id"
              />
            </div>
          </td>
          <td class="table-4__data">
            3 Points
          </td>
          <td class="table-4__data">
            <div class="flex flex-col items-center md:block">
              <Input
                name="three_pts_made"
                :value="awayStats.three_pts_made"
                :statId="awayStats.id"
              />
              /
              <Input
                name="three_pts_att"
                :value="awayStats.three_pts_att"
                :statId="awayStats.id"
              />
            </div>
          </td>
        </tr>

        <AnalysisTableRow 
          :col1="homeStats.three_pts_percentage"
          col2="%"
          :col3="awayStats.three_pts_percentage"
        />

        <AnalysisTableRow 
          :col1="homeStats.total_made + '/' + homeStats.total_att"
          col2="Total Field Goals"
          :col3="awayStats.total_made + '/' + awayStats.total_att"
        />

        <AnalysisTableRow 
          :col1="homeStats.total_fg_percentage"
          col2="%"
          :col3="awayStats.total_fg_percentage"
        />

        <tr>
          <td class="table-4__data">
            <div class="flex flex-col items-center md:block">
              <Input
                name="ft_made"
                :value="homeStats.ft_made"
                :statId="homeStats.id"
              />
              /
              <Input
                name="ft_att"
                :value="homeStats.ft_att"
                :statId="homeStats.id"
              />
            </div>
          </td>
          <td class="table-4__data">
            Free Throws
          </td>
          <td class="table-4__data">
            <div class="flex flex-col items-center md:block">
              <Input
                name="ft_made"
                :value="awayStats.ft_made"
                :statId="awayStats.id"
              />
              /
              <Input
                name="ft_made"
                :value="awayStats.ft_made"
                :statId="awayStats.id"
              />
            </div>
          </td>
        </tr>

        <AnalysisTableRow 
          :col1="homeStats.ft_percentage"
          col2="%"
          :col3="awayStats.ft_percentage"
        />

        <tr>
          <td class="table-4__data">
            <Input 
              name="reb_off"
              :value="homeStats.reb_off"
              :statId="homeStats.id"
            />
          </td>
          <td class="table-4__data">
            Offensive Rebounds
          </td>
          <td class="table-4__data">
            <Input 
              name="reb_off"
              :value="awayStats.reb_off"
              :statId="awayStats.id"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input 
              name="reb_def"
              :value="homeStats.reb_def"
              :statId="homeStats.id"
            />
          </td>
          <td class="table-4__data">
            Defensive Rebounds
          </td>
          <td class="table-4__data">
            <Input 
              name="reb_def"
              :value="awayStats.reb_def"
              :statId="awayStats.id"
            />
          </td>
        </tr>

        <AnalysisTableRow 
          :col1="homeStats.reb_total"
          col2="Total Rebounds"
          :col3="awayStats.reb_total"
        />

        <tr>
          <td class="table-4__data">
            <Input 
              name="steals"
              :value="homeStats.steals"
              :statId="homeStats.id"
            />
          </td>
          <td class="table-4__data">
            Steals
          </td>
          <td class="table-4__data">
            <Input 
              name="steals"
              :value="awayStats.steals"
              :statId="awayStats.id"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input 
              name="assists"
              :value="homeStats.assists"
              :statId="homeStats.id"
            />
          </td>
          <td class="table-4__data">
            Assists
          </td>
          <td class="table-4__data">
            <Input 
              name="assists"
              :value="awayStats.assists"
              :statId="awayStats.id"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input 
              name="blocks"
              :value="homeStats.blocks"
              :statId="homeStats.id"
            />
          </td>
          <td class="table-4__data">
            Blocks
          </td>
          <td class="table-4__data">
            <Input 
              name="blocks"
              :value="awayStats.blocks"
              :statId="awayStats.id"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input 
              name="turnovers"
              :value="homeStats.turnovers"
              :statId="homeStats.id"
            />
          </td>
          <td class="table-4__data">
            Turnovers
          </td>
          <td class="table-4__data">
            <Input 
              name="turnovers"
              :value="awayStats.turnovers"
              :statId="awayStats.id"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input2 
              name="off_turnover"
              :value="homePointsClassification.off_turnover"
              :classificationId="homePointsClassification.id"
              type="classification"
            />
          </td>
          <td class="table-4__data">
            Points Off Turnover
          </td>
          <td class="table-4__data">
            <Input2 
              name="off_turnover"
              :value="awayPointsClassification.off_turnover"
              :classificationId="awayPointsClassification.id"
              type="classification"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input2 
              name="second_chance"
              :value="homePointsClassification.second_chance"
              :classificationId="homePointsClassification.id"
              type="classification"
            />
          </td>
          <td class="table-4__data">
            2nd Chance Points
          </td>
          <td class="table-4__data">
            <Input2 
              name="second_chance"
              :value="awayPointsClassification.second_chance"
              :classificationId="awayPointsClassification.id"
              type="classification"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input2 
              name="fast_break"
              :value="homePointsClassification.fast_break"
              :classificationId="homePointsClassification.id"
              type="classification"
            />
          </td>
          <td class="table-4__data">
            Fast Break Points
          </td>
          <td class="table-4__data">
            <Input2 
              name="fast_break"
              :value="awayPointsClassification.fast_break"
              :classificationId="awayPointsClassification.id"
              type="classification"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input2 
              name="starters"
              :value="homePointsClassification.starters"
              :classificationId="homePointsClassification.id"
              type="classification"
            />
          </td>
          <td class="table-4__data">
            Starters Points
          </td>
          <td class="table-4__data">
            <Input2 
              name="starters"
              :value="awayPointsClassification.starters"
              :classificationId="awayPointsClassification.id"
              type="classification"
            />
          </td>
        </tr>

        <tr>
          <td class="table-4__data">
            <Input2 
              name="bench"
              :value="homePointsClassification.bench"
              :classificationId="homePointsClassification.id"
              type="classification"
            />
          </td>
          <td class="table-4__data">
            Bench Points
          </td>
          <td class="table-4__data">
            <Input2 
              name="bench"
              :value="awayPointsClassification.bench"
              :classificationId="awayPointsClassification.id"
              type="classification"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { inject } from 'vue';

  import AnalysisTableRow from './AnalysisTableRow.vue';
  import Input from './Input.vue';
  import Input2 from './Input2.vue';

  export default {
    components: {
      AnalysisTableRow,
      Input,
      Input2
    },
    props: {
      homeStats: {},
      awayStats: {},
      homePointsClassification: {},
      awayPointsClassification: {},
      name: String
    },
    setup(props) {
      const game = inject('game', game)

      return {
        game,
        ...props
      }
    }
  }
</script>