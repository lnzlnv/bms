<template>
  <div>
    <div 
      v-if="modalIsOpen"
      class="modal-1 flex items-center px-[1em] md:px-0"
    >
      <EditForm 
        :team="options.id"
        :options="options"
        :selectedPlayer="selectedPlayer"
        :season="season"
        :isEdited="isEdited"
        :editSuccess="editSuccess"
      />
    </div>

    <div 
      v-if="isLoading"
      class="loading flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[100000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="playerIsEdited"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Player has been successfully edited!
      </div>
    </div>

    <div
      v-if="playerIsDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Player has been successfully deleted!
      </div>
    </div>

    <div class="mx-[10vw] mb-[4rem]">
      <h1 class="schedule__title bg-skew-2 w-max mb-[1rem]">
        {{ options.name }}
      </h1>
    
      <div class="mb-0 md:grid md-grid-3-column-1 items-center justify-between">
        <div class="mb-[1rem] md:mb-0">
          <a
            class="btn-12"
            :href="options.create_player_url"
          >
            Add Player
          </a>
        </div>
        <div class="mb-[1rem] md:mb-0">
          <img
            class="img-7"
            :src="options.logo"
            alt=""
          />
        </div>
        <form class="md:flex justify-end items-start gap-[20px] mb-[2rem] md:mb-0">
          <div>
            <select
              v-model="season"
              class="input-field-5 w-full"
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
        </form>
      </div>
      <table class="table-1">
        <thead>
          <tr>
            <th class="table-1__header text-left">First Name</th>
            <th class="table-1__header text-left">Last Name</th>
            <th class="table-1__header text-center">Number</th>
            <th class="table-1__header text-center">Height</th>
            <th class="table-1__header text-center">Weight</th>
            <th class="table-1__header text-left"></th>
          </tr>
        </thead>
        <tbody
          v-if="Object.keys(players).length != 0"
        >
          <tr
            v-for="player in players"
            :key="player.id"
            class="table-1__row flex flex-col lg:table-row"
          >
            <td
              class="table-1__data text-left lg:table-cell"
              data-cell="First Name"
            >
              {{ player.first_name }}
            </td>
            <td
              class="table-1__data text-left lg:table-cell"
              data-cell="Last Name"
            >
              {{ player.last_name }}
            </td>
            <td
              class="table-1__data lg:text-center lg:table-cell"
              data-cell="Number"
            >
              {{ player.player_number }}
            </td>
            <td
              class="table-1__data lg:text-center lg:table-cell"
              data-cell="Height"
            >
              {{ player.height }}
            </td>
            <td
              class="table-1__data lg:text-center lg:table-cell"
              data-cell="Weight"
            >
              {{ player.weight }}
            </td>
            <td
              class="table-1__data empty text-left lg:table-cell"
            >
              <div class="grid grid-2-column-2">
                <button
                  @click="openEditModal(player.player_number)"
                  class="btn-9 mr-[0.5rem] text-center"
                >
                  Edit
                </button>
                <button
                  @click="deletePlayer(player.id)"
                  class="btn-10"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr class="table-1__row flex flex-col lg:table-row">
            <td 
              class="table-1__data empty lg:table-cell"
              colspan="6"
            >
              No available players.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>  
  import axios from 'axios';
  import { computed, onBeforeMount, ref, watch, provide } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import setCsrfToken from '@composables/csrf-token.js';
  import host from '@composables/host.js';
  import normalizeData from '@composables/normalize-data-3.js'
  import EditForm from './EditForm.vue';
  import success from '@composables/generate-account/success.js'

  setCsrfToken()

  export default {
    components: {
      EditForm, 
      LoadingSpinner
    },
    setup() {
      const options = ref({})
      const season = ref(0)
      const players = ref({})
      const modalIsOpen = ref(false)
      const selectedPlayer = ref({})
      const playerIsEdited = success()
      const playerIsDeleted = success()
      const isEdited = success()
      const hasError = success()
      const isLoading = ref(false)
      
      const allUrl = computed(() => {
        return host + '/api/season-' + season.value +'/' 
        + options.value.id + '/players/'
      })

      onBeforeMount(() => {
        isLoading.value = true
        const teamId = document.getElementById('js-team-id').value
        const url = host + '/api/team/players/options/' + teamId + '/'

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            season.value = response.data.current_season.id
            
            getPlayers(allUrl.value)
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      /**
       * Methods
       */
        const getPlayers = (url) => {
          isLoading.value = true
          axios
            .get(url)
            .then(response => {
              players.value = normalizeData(response.data)
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const deletePlayer = (id) => {
          isLoading.value = true
          const url = host + '/api/' 
            + season.value + '/' + id  +'/players/'

          axios
            .delete(url)
            .then(response => {
              playerIsDeleted.value = true
              getPlayers(allUrl.value)
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        } 

        const openEditModal = (id) => {
          selectedPlayer.value = players.value[id]
          selectedPlayer.value['season'] = season.value
          modalIsOpen.value = true
        }

        const editSuccess = () => {
          playerIsEdited.value = true
          modalIsOpen.value = false
        }
      /**
       * End of Methods
       */

      /**
       * Watch
       */
        watch(
          season,
          () => {
            getPlayers(allUrl.value)
          }
        )
      /**
       * End of Watch
       */

      provide('modalIsOpen', modalIsOpen)
      provide('hasError', hasError)

      return {
        options,
        season,
        players,
        playerIsDeleted,
        playerIsEdited,
        modalIsOpen,
        isEdited,
        selectedPlayer,
        hasError,
        isLoading,
        getPlayers,
        deletePlayer,
        openEditModal,
        editSuccess
      }
    }
  }
</script>