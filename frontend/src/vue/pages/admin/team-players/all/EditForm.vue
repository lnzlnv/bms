<template>
  <div class="container-7 relative">
    <div 
      v-if="isLoading"
      class="loading-2 flex justify-center items-center"
    >
      <LoadingSpinner />
    </div>

    <div class="text-right mb-[1rem]">
      <button
        @click="modalIsOpen = false"
      >
        <img 
        class="icon-2"
        :src="closeIcon" 
        alt="close icon"
      />
      </button>
    </div>

    <form
      @submit.prevent="editPlayer"
    >
      <div class="non-field-errors mb-[1rem]">
        <Errors 
          :errors="errors.non_field_errors"
        />
      </div>

      <div class="mb-[1rem]">
        <select
          v-model="selectedPlayer.season"
          class="input-field-3"
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
          v-model="selectedPlayer.first_name"
          class="input-field-3"
          type="text"
          placeholder="First Name"
        >

        <Errors 
          :errors="errors.first_name"
        />
      </div>

      <div class="mb-[1rem]">
        <input 
          v-model="selectedPlayer.last_name"
          class="input-field-3"
          type="text"
          placeholder="Last Name"
        >
        <Errors 
          :errors="errors.last_name"
        />
      </div>

      <div class="mb-[1rem]">
        <input 
          v-model="selectedPlayer.position"
          class="input-field-3"
          type="text"
          placeholder="Position"
        >

        <Errors 
          :errors="errors.position"
        />
      </div>

      <div class="mb-[1rem]">
        <input 
          v-model="selectedPlayer.player_number"
          class="input-field-3"
          type="number"
          placeholder="Player Number"
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
              v-model="selectedPlayer.height_feet"
              class="input-field-3"
              type="number"
              placeholder="Feet"
            >

            <Errors 
            :errors="errors.height_feet"
          />
          </div>

          <div>
            <input
              v-model="selectedPlayer.height_inches"
              class="input-field-3"
              type="number"
              max="11"
              placeholder="Inches"
            >

            <Errors 
              :errors="errors.height_inches"
            />
          </div>
        </div>
      </div>

      <div>
        <input  
          v-model="selectedPlayer.weight"
          class="input-field-3"
          type="number"
          placeholder="Weight"
        >

        <Errors 
          :errors="errors.weight"
        />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Edit Player</button>
      </div>
    </form>
  </div>
</template>

<script>
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import host from '@composables/host.js';
  import setCsrfToken from '@composables/csrf-token.js';
  import closeIcon from '@images/close-icon.svg'
  import { inject, ref } from 'vue';
  import axios from 'axios';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  setCsrfToken()

  export default {
    components: {
      Errors,
      LoadingSpinner
    },
    props: {
      options: {},
      season: Number,
      selectedPlayer: {},
      team: Number,
      editSuccess: Function
    },
    setup(props) {
      const errors = ref({})
      const isLoading = ref(false)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const hasError = inject('hasError', hasError)
      
      const editPlayer = () => {
        isLoading.value = true
        const url = host + '/api/' + props.team 
          + '/player-' + props.selectedPlayer.id + '/'

        axios
          .put(url, props.selectedPlayer)
          .then(response => {
            props.editSuccess()
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            if (err.request == undefined || err.request.status != 400) {
              hasError.value= true
              return 
            }

            errors.value = err.response.data
          })
      }

      return {
        ...props,
        errors,
        closeIcon,
        modalIsOpen,
        isLoading,
        editPlayer
      }
    }
  }
</script>