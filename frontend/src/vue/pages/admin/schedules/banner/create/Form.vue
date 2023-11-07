<template>
  <div class="relative">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="bannerIsCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Schedule Banner has been successfully created!
      </div>
    </div>

    <div class="max-w-[800px] mx-auto">
      <form 
        @submit.prevent="createBanner"
        class="form-1 p-[1em]"
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
            v-model="banner.season"
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
          <select
            v-model="banner.division"
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

        <div class="mb-[1rem]">
          <input 
            v-model="banner.date"
            class="input-field-3"
            type="datetime-local" 
            name="expiration_date" 
            id="expiration_date"
            required="required"
            title="Expiration Date"
          >
          <Errors
            :errors="errors.date"
          />
        </div>

        <div>
          <input 
            @change="addImage"
            class="input-field-3"
            type="file"
            accept=".png"
            ref="image"
            id="image"
            hidden="hidden"
          >

          <DragArea 
            forInput="image"
            dragAreaName="js-drag-area"
            :imageUrl="imageUrl"
          />

          <Errors
            :errors="errors.image"
          />
        </div>

        <div class="text-right">
          <button class="btn-7 mt-[1rem]">Create Banner</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import { onBeforeMount, onMounted, reactive, ref, watch } from 'vue';
  import axios from 'axios'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import host from '@composables/host.js';
  import setCsrfToken from '@composables/csrf-token.js';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import success from '@composables/generate-account/success.js'
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
      const options = ref({})
      const bannerIsCreated = success()
      const isLoading = ref(false)
      const image = ref(null)
      const errors = ref({})
      const hasError = success()
      const banner = reactive({
        season: '',
        division: '',
        date: '',
        image: null
      })
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop('js-drag-area', imageUrl, banner, 'image')
      })

      onBeforeMount(() => {
        isLoading.value = true
        const url = host + '/api/game-schedule/banner/options/'
        axios
          .get(url)
          .then(response => {
            options.value = response.data
            banner.season = response.data.current_season.id
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      const addImage = () => {
        banner.image = image.value.files[0]

        if (banner.image) {
          imageUrl.value = URL.createObjectURL(banner.image)
          return
        }
        
        imageUrl.value = null
      }

      const createBanner = () => {
        isLoading.value = true
        const url = host + '/api/game-schedule/banner/'
        
        axios
          .post(
            url, 
            banner,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            bannerIsCreated.value = true
            banner.division = response.data.division
            banner.date = ''

            image.value.value = ''
            image.value.files = new DataTransfer().files

            errors.value = {}
            imageUrl.value = null
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
        bannerIsCreated,
        banner,
        isLoading,
        image,
        errors,
        hasError,
        imageUrl,
        addImage,
        createBanner,
      }
    }
  }
</script>