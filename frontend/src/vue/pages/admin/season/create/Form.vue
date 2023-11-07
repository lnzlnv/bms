<template>
  <div class="max-w-[800px] mx-auto px-[1em] mb-[4rem] relative">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="seasonIsCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Season has been successfully created!
      </div>
    </div>

    <form 
      @submit.prevent="createSeason"
      class="form-1 p-[1em]"
    >
      <div 
        v-if="isLoading"
        class="loading-2 flex justify-center items-center"
      >
        <LoadingSpinner />
      </div>

      <Errors 
        :errors="errors.non_field_errors"
      />

      <div class="mb-[1rem]">
        <input
          v-model="newSeason.year"
          class="input-field-3"
          type="number"
          placeholder="Season Number"
          required="required"
        />
        
        <Errors 
          :errors="errors.year"
        />
      </div>

      <div>
        <input 
          @change="addLogo"
          class="input-field-3"
          type="file" 
          accept="image/*" 
          ref="logo"
          id="logo"
          hidden
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
        <button class="btn-7 mt-[1rem]">Create New Season</button>
      </div>
    </form>
  </div>
</template>

<script>
  import axios from 'axios';

  import host from '@composables/host.js';
  import setCsrfToken from '@composables/csrf-token.js';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import success from '@composables/generate-account/success.js'
  import { onMounted, reactive, ref, watch } from 'vue';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';

  setCsrfToken()

  export default {
    components: {
      Errors,
      LoadingSpinner,
      DragArea
    },
    setup() {
      const newSeason = reactive({
        year: null,
        logo: null
      })
      const logo = ref(null)
      const seasonIsCreated = success()
      const errors = ref({})
      const isLoading = ref(false)
      const hasError = error()
      const logoUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop(
          'js-drag-area',
          logoUrl,
          newSeason,
          'logo'
        )
      })

      const createSeason = () => {
        isLoading.value = true
        const url = host + '/api/seasons/'

        axios
          .post(
            url, 
            newSeason,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            seasonIsCreated.value = true
            newSeason.logo = null
            newSeason.year = null

            logo.value.value = ''
            logo.value.files = new DataTransfer().files
            errors.value = {}
            logoUrl.value = null
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            if (err.request == undefined || err.request.status != 400) {
              hasError.value = true
              return
            }

            errors.value = err.response.data
          })
      }

      const addLogo = () => {
        newSeason.logo = logo.value.files[0]

        if (newSeason.logo) {
          logoUrl.value = URL.createObjectURL(newSeason.logo)
          return
        }
        
        logoUrl.value = null
      }

      return {
        newSeason,
        isLoading,
        logo,
        errors,
        seasonIsCreated,
        hasError,
        logoUrl,
        createSeason,
        addLogo,
      }
    }
  }
</script>