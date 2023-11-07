<template>
  <form
    @submit.prevent="createPlayer"
    class="form-1 p-[1em] relative"
  >
    <div 
      v-if="isLoading"
      class="loading-2 flex justify-center items-center"
    >
      <LoadingSpinner />
    </div>

    <div class="non-field-errors mb-[1rem]">
      <Errors 
        :errors="errors.non_field_errors"
      />
    </div>

    <div class="mb-[1rem]">
      <select
        v-model="newPlayer.season"
        class="input-field-3"
        required="required"
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

      <Errors 
        :errors="errors.season"
      />
    </div>
    <div class="mb-[1rem]">
      <input 
        v-model="newPlayer.first_name"
        class="input-field-3"
        type="text"
        placeholder="First Name"
        required="required"
        name="first_name"
      >

      <Errors 
        :errors="errors.first_name"
      />
    </div>

    <div class="mb-[1rem]">
      <input 
        v-model="newPlayer.last_name"
        class="input-field-3"
        type="text"
        placeholder="Last Name"
        name="last_name"
        required="required"
      >
      <Errors 
        :errors="errors.last_name"
      />
    </div>

    <div class="mb-[1rem]">
      <input 
        v-model="newPlayer.position"
        class="input-field-3"
        type="text"
        placeholder="Position"
        required="required"
      >

      <Errors 
        :errors="errors.position"
      />
    </div>

    <div class="mb-[1rem]">
      <input 
        v-model="newPlayer.player_number"
        class="input-field-3"
        type="number"
        placeholder="Player Number"
        required="required"
      >
      <Errors 
        :errors="errors.player_number"
      />
    </div>

    <div>
      <div class="label-4">Height:</div>
      <div class="mb-[1rem] grid grid-2-column-2 gap-[10px]">
        <div>
          <input
            v-model="newPlayer.height_feet"
            class="input-field-3"
            type="number"
            placeholder="Feet"
            required="required"
          >

          <Errors 
          :errors="errors.height_feet"
        />
        </div>

        <div>
          <input
            v-model="newPlayer.height_inches"
            class="input-field-3"
            type="number"
            max="11"
            placeholder="Inches"
            required="required"
          >

          <Errors 
            :errors="errors.height_inches"
          />
        </div>
      </div>
    </div>

    <div>
      <input  
        v-model="newPlayer.weight"
        class="input-field-3"
        type="number"
        placeholder="Weight"
        required="required"
      >

      <Errors 
        :errors="errors.weight"
      />
    </div>

    <div class="text-right">
      <button class="btn-7 mt-[1rem]">Add Player</button>
    </div>
  </form>
</template>

<script>
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import host from '@composables/host.js';
  import setCsrfToken from '@composables/csrf-token.js';
  import { inject, ref } from 'vue';
  import axios from 'axios';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  setCsrfToken()

  export default {
    components: {
      Errors,
      LoadingSpinner
    },
    setup() {
      const errors = ref({})
      const options = inject('options', options)
      const newPlayer = inject('newPlayer', newPlayer)
      const playerIsCreated = inject('playerIsCreated', playerIsCreated)
      const isLoading = inject('isLoading', isLoading)
      const hasError = inject('hasError', hasError)

      const createPlayer = () => {
        isLoading.value = true
        const url = host + '/api/' + newPlayer.season + '/' 
          + options.value.id + '/players/';
        
        axios
          .post(url, newPlayer)
          .then(response => {
            playerIsCreated.value = true
            errors.value = {}
            
            for (const key in newPlayer) {
              if (key == 'team' || key == 'season') {
                continue
              }
              
              newPlayer[key] = ''
            }
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            if (err.request.status == 400) {
              errors.value = err.response.data
              return
            }

            hasError.value = true
          })
      }

      return {
        options,
        newPlayer,
        errors,
        options,
        isLoading,
        createPlayer
      }
    }
  }
</script>