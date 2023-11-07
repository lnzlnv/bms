<template>
  <div>
    <form
      @submit.prevent="performSubstitution"
      class="max-w-[350px] mx-[auto]"
    >
      <div class="grid grid-2-column-2 gap-[10px] mb-[1rem]">
        <input 
          v-model="substitutionData.minutes"
          class="input-field-3"
          type="number" 
          placeholder="Minutes"
          required="required"
        >
        <input 
          v-model="substitutionData.seconds"
          type="number" 
          class="input-field-3"
          placeholder="Seconds"
          required="required"
        >
      </div>

      <button class="btn-12 sub">
          Substitute
        </button>
    </form>

    <div class="grid md-grid-2-column-2 gap-[50px]">
      <div class="substitution__panel">
        <h2 class="substitution__label in">IN</h2>
        <div class="substitution__panel-content in">
          <ul v-if="activeTeamSubstitution != null">
            <li 
              v-for="player in activeTeamSubstitution.in"
              :key="player.id"
              class="substitution__player"
            >
              {{ player.number }} - {{ player.name }}
            </li>
          </ul>
        </div>
      </div>
      <div class="substitution__panel out">
        <h2 class="substitution__label out">OUT</h2>
        <div class="substitution__panel-content out">
          <ul v-if="activeTeamSubstitution != null">
            <li 
              v-for="player in activeTeamSubstitution.out"
              :key="player.id"
              class="substitution__player"
            >
              {{ player.number }} - {{ player.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { computed, inject, ref } from 'vue';

  import setCsrfToken from '@composables/csrf-token.js';
  import host from '@composables/host.js';
import axios from 'axios';

  setCsrfToken()

  export default {
    setup() {
      const game = inject('game', game)
      const activeTeam = inject('activeTeam', activeTeam)
      const substitution = inject('substitution', substitution)
      const roomMemberUniqueID = inject('roomMemberUniqueID', roomMemberUniqueID)
      const substitutionData = inject('substitutionData', substitutionData)
      const inGameHomePlayers = inject('inGameHomePlayers', inGameHomePlayers)
      const inGameAwayPlayers = inject('inGameAwayPlayers', inGameAwayPlayers)
      const periods = inject('periods', periods)
      const addSuccessMessage = inject('addSuccessMessage', addSuccessMessage)
      const endOfAQuarter = ref(false)
      const isLoading = inject('isLoading', isLoading)

      const activeTeamSubstitution = computed(() => {
        if (activeTeam.value == null) {
          return 
        }

        if (activeTeam.value == game.value.home_team.id) {
          return substitution.homeTeam
        } else {
          return substitution.awayTeam
        }

      })

      const performSubstitution = () => {
        const activeTeamIsHome = activeTeam.value == game.value.home_team.id
        const inGamePlayers = activeTeamIsHome ? 
          inGameHomePlayers.value : inGameAwayPlayers.value

        const team = activeTeamIsHome ? 
          substitution.homeTeam : substitution.awayTeam
        if (!fivePlayersIsInGame(team, inGamePlayers)) {
          return
        }

        setSubInAndOut(activeTeamIsHome)

        endOfAQuarter.value = substitutionData.minutes == 0 && substitutionData.seconds == 0
        const hasSubIn = Object.keys(substitutionData.sub_in).length > 0

        if (endOfAQuarter.value && hasSubIn) {
          addSuccessMessage({
            content: 'Quarter has ended. Cannot sub-in players.',
            class: 'delete-1'
          })
          return
        }

        addAllPlayersToOut()

        substitutionData['sub_out_all'] = endOfAQuarter.value
        substitutionData['quarter'] = periods.value

        sendMessageOnSocket()

        // reset substitution container
        team.in = {}
        team.out = {}
      }

      const fivePlayersIsInGame = (team, inGamePlayers) => {
        let inGamePlayersIsFive = true

        if(!endOfAQuarter.value) {
          const inGamePlayersNumber = Object.keys(inGamePlayers).length
        
          const subInPlayersNumber = Object.keys(team.in).length
          const subOutPlayersNumber = Object.keys(team.out).length

          const newInGamePlayersNumber = (inGamePlayersNumber + subInPlayersNumber) - subOutPlayersNumber

          inGamePlayersIsFive = newInGamePlayersNumber == 5

          if (!inGamePlayersIsFive) {
            addSuccessMessage({
              content: 'Please make sure the in-game players is 5.',
              class: 'delete-1'
            })
          }
        }

        return inGamePlayersIsFive
      }

      const setSubInAndOut = (activeTeamIsHome) => {
        if (activeTeamIsHome) {
          substitutionData.sub_in = 
            getPlayerListInSpaceSeparatedString(substitution.homeTeam.in)
          substitutionData.sub_out = 
            getPlayerListInSpaceSeparatedString(substitution.homeTeam.out)
        } else {
          substitutionData.sub_in = 
            getPlayerListInSpaceSeparatedString(substitution.awayTeam.in)
          substitutionData.sub_out = 
            getPlayerListInSpaceSeparatedString(substitution.awayTeam.out)
        }
      }

      const addAllPlayersToOut = () => {
        if (!endOfAQuarter.value) {
          return
        }

        const homeTeam = 
            getPlayerListInSpaceSeparatedString(inGameHomePlayers.value)
        const awayTeam =
        getPlayerListInSpaceSeparatedString(inGameAwayPlayers.value)
        substitutionData.sub_out = homeTeam + awayTeam
      }

      const getPlayerListInSpaceSeparatedString = (players) => {
        let temp = ''

        for (let player_id in players) {
          temp += player_id + ' '
        }
        return temp
      }

      const socket = inject('socket', socket)

      const sendMessageOnSocket = () => {
        const data = {
          type: 'substitution',
          content: substitutionData,
          game_id: game.value.id,
          team_id: activeTeam.value,
          room_member_id: roomMemberUniqueID,
          message: {
            class: 'success-2',
            content: 'Players has been substituted successfully!',
          },
          statistician: game.value.statistician.id
        }
        isLoading.value = true
        socket.value.send(JSON.stringify(data))
      }

      return {
        activeTeamSubstitution,
        substitutionData,
        performSubstitution
      }
    }
  }
</script>