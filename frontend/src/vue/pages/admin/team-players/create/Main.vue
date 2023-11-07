<template>
  <div class="max-w-[800px] mx-auto px-[1em] mb-[4rem] relative">
    <div 
      v-if="playerIsCreated"
      class="container-8 flex justify-center"
    >
      <div class="success-1">
        Player has been successfully created!
      </div>
    </div>

    <div 
      v-if="hasError"
      class="container-8 flex justify-center z-[100000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div>
      <a 
        :href="options.players_url"
      >
        <img 
          class="img-8"
          :src="goBackIcon" 
          alt=""
        />
      </a>
    </div>

    <div class="mb-[1rem]">
      <img 
        class="img-7"
        :src="options.logo" 
        alt=""
      />
    </div>

    <h1 class="schedule__title bg-skew-2 w-max mb-[2rem]">
      {{ options.name }}
    </h1>

    <div class="text-right mb-[1rem]">
      <button 
        v-if="!importPlayer"
        @click="importPlayer = true"
        class="btn-12"
      >
        Import Player
      </button>

      <button
        v-else
        @click="importPlayer = false"
        class="btn-12"
      >
        New Player
      </button>
    </div>

    <PlayerImport v-show="importPlayer" />
    <Form v-show="!importPlayer" />
  </div>
</template>

<script>
  import host from '@composables/host.js';
  import setCsrfToken from '@composables/csrf-token.js';
  import goBackIcon from '@images/go-back.png'
  import success from '@composables/generate-account/success.js'
  import { onBeforeMount, provide, reactive, ref, watch } from 'vue';
  import axios from 'axios';
  import Form from './Form.vue';
  import PlayerImport from './PlayerImport.vue'

  setCsrfToken()

  export default {
    components: {
      Form,
      PlayerImport
    },
    setup() {
      const options = ref({})
      const importPlayer = ref(false)
      const isLoading = ref(false)
      const playerIsCreated = success()
      const hasError = success()
      const newPlayer = reactive({
        season: '',
        first_name: '',
        last_name: '',
        position: '',
        player_number: '',
        height_feet: '',
        height_inches: '',
        weight: '',
        team: '',
      })
      const teamId = document.getElementById('js-team-id').value

      onBeforeMount(() => {
        isLoading.value = true
        const url = host + '/api/team/players/options/' + teamId + '/';

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            newPlayer.season = response.data.current_season.id
            newPlayer.team = response.data.id
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      provide('options', options)
      provide('newPlayer', newPlayer)
      provide('playerIsCreated', playerIsCreated)
      provide('teamId', teamId)
      provide('isLoading', isLoading)
      provide('hasError', hasError)

      return {
        options,
        playerIsCreated,
        goBackIcon,
        importPlayer,
        hasError
      }
    }
  }
</script>