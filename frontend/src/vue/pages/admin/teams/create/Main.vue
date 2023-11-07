<template>
  <div class="relative">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="teamIsCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Team has been successfully created!
      </div>
    </div>

    
    <div class="max-w-[800px] px-[1em] mx-auto">
      <NewTeamForm v-show="activeTab == 1" />
      <ImportTeamForm v-show="activeTab == 2" />
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { onBeforeMount, ref, watch, provide, reactive } from 'vue';

  import setCsrfToken from '@composables/csrf-token.js';
  import { error } from './composables.js'
  import NewTeamForm from './NewTeamForm.vue'
  import ImportTeamForm from './ImportTeamForm.vue';

  setCsrfToken()

  export default {
    name: 'Form',
    components: {
      NewTeamForm,
      ImportTeamForm
    },
    setup() {
      const teamIsCreated = ref(false)
      const options = ref({})
      const hasError = error()
      const activeTab = ref(1)
      const isLoading = ref(false)

      onBeforeMount(() => {
        isLoading.value = true
        const url = '/api/teams/create/options/';

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      /**
       * Watch
       */
        watch(
          teamIsCreated,
          (isCreated) => {
            if (isCreated) {
              setTimeout(() => {
                teamIsCreated.value = false
              }, 5000)
            }
          }
        )
      /**
       * End of Watch
       */

      provide('teamIsCreated', teamIsCreated)
      provide('hasError', hasError)
      provide('options', options)
      provide('activeTab', activeTab)
      provide('isLoading', isLoading)

      return {
        teamIsCreated,
        options,
        hasError,
        activeTab
      }
    }
  }
</script>