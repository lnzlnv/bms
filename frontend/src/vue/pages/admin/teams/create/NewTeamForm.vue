<template>
  <div>
    <div class="text-right mb-[1rem]">
      <button 
        @click="activeTab = 2"
        class="btn-12"
      >
        Import Team
      </button>
    </div>

    <form @submit.prevent="createTeam" class="form-1 p-[1em] relative">
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
          v-model="team.season"
          class="input-field-3"
          required="required"
        >
        <option value="" disabled selected>Select Season</option>
        <option
          v-for="season in options.seasons"
          :key="season.id"
          :value="season.year"
        >
          {{ season.year }}
        </option>
        </select>
        <Errors
          :errors="errors.division"
        />
      </div>
      <div class="mb-[1rem]">
        <input
          v-model="team.name"
          class="input-field-3"
          type="text"
          name="name"
          id="name"
          placeholder="Name"
          required="required"
        />
        <Errors
          :errors="errors.name"
        />
      </div>
      <div class="mb-[1rem]">
        <select
          v-model="team.division"
          class="input-field-3"
          required="required"
        >
        <option value="" disabled selected>Select Division</option>
        <option
          v-for="division in options.divisions"
          :key="division[0]"
          :value="division[0]"
        >
          {{ division[1] }}
        </option>
        </select>
        <Errors
          :errors="errors.division"
        />
      </div>
      <div>
        <input
          @change="addLogo"
          class="input-field-3"
          type="file"
          accept=".png"
          ref="logo"
          id="logo"
          hidden="hidden"
        >

        <DragArea 
          :imageUrl="logoUrl"
          forInput="logo"
          dragAreaName="js-drag-area"
        />

        <Errors
          :errors="errors.logo"
        />
      </div>
      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Create Team</button>
      </div>
    </form>
  </div>
</template>
<script>
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import axios from 'axios';
  import { inject, onMounted, reactive, ref, watch } from 'vue';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  
  export default {
    components: {
      Errors,
      DragArea,
      LoadingSpinner
    },
    setup() {
      const errors = ref({})
      const logo = ref(null)
      const teamIsCreated = inject('teamIsCreated', teamIsCreated)
      const hasError = inject('hasError', hasError)
      const options = inject('options', options)
      const team = reactive({
        name: '',
        division: '',
        logo: '',
        season: ''
      })
      const activeTab = inject('activeTab', activeTab)
      const logoUrl = ref(null)
      const isLoading = inject('isLoading', isLoading)
    
      onMounted(() => {
        fileDragAndDrop('js-drag-area', logoUrl, team, 'logo')
      })

      /**
       * Watch
       */
        watch(
          options,
          () => {
            team.season = options.value.seasons[0].year
          }
        )
      /**
       * End of Watch
       */

      /**
       * Methods
       */
        const createTeam = () => {
          isLoading.value = true
          const url = '/api/teams/';

          axios
            .post(
              url, 
              team,
              {
                headers: {
                  'Content-Type': 'multipart/form-data',
                },
              }
            )
            .then(response => {
              teamIsCreated.value = true
              team.name = ''
              team.division = ''
              logo.value.value = ''
              logo.value.files = new DataTransfer().files
              logoUrl.value = null
              errors.value = {}
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              if (err.response.status != 400) {
                hasError.value = true
              }
              
              errors.value = err.response.data
            })
        }

        const addLogo = (event) => {
          team.logo = event.target.files[0]

          if (team.logo) {
            logoUrl.value = URL.createObjectURL(team.logo)
            return
          }
          
          logoUrl.value = null
        }
      /**
       * End of Methods
       */
      return {
        team,
        options,
        errors,
        activeTab,
        logoUrl,
        logo,
        isLoading,
        addLogo,
        createTeam,
      }
    }
  }
</script>