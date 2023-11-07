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
      v-if="isCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Highlight has been successfully added!
      </div>
    </div>

    <form
      @submit.prevent="addHighlights"
      class="form-1 p-[1em] relative"
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

      <div>
        <input
          @change="setVideo"
          ref="video"
          class="input-field-3"
          type="file"
          name="highlights"
          id="highlights"
          accept="video/*"
          hidden="hidden"
        />

        <DragAreaVideo 
          :videoUrl="videoUrl"
          forInput="highlights"
          dragAreaName="js-drag-area"
          :videoType="videoType"
        />

        <Errors 
        :errors="errors.video"
      />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Add Highlights</button>
      </div>                                        
    </form>
  </div>
</template>
<script>
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import { onMounted, ref } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import setCsrfToken from '@composables/csrf-token.js';
  import success from '@composables/generate-account/success.js'
  import axios from 'axios';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragAreaVideo from '@components/DragAreaVideo.vue';

  setCsrfToken()

  export default {
    components: {
      Errors,
      LoadingSpinner,
      DragAreaVideo
    },
    setup() {
      const errors = ref({})
      const isLoading = ref(false)
      const video = ref(null)
      const data = {
        video: null
      }
      const isCreated = success()
      const hasError = success()
      const videoUrl = ref(null)
      const videoType = ref(null)

      onMounted(() => {
        fileDragAndDrop(
          'js-drag-area', 
          videoUrl, 
          data, 
          'video',
          'video',
          videoType
        )
      })


      /**
       * Methods
       */
        const setVideo = () => {
          data.video = video.value.files[0]

          if (data.video) {
            videoUrl.value = URL.createObjectURL(data.video)
            return
          }

          videoUrl.value = null
        }

        const addHighlights = () => {
          isLoading.value = true

          const url = '/api/landing/highlights/'

          axios
            .post(
              url, 
              data,
              {
                headers: {
                  'Content-Type': 'multipart/form-data',
                },
              }
            )
            .then(response => {
              isLoading.value = false
              isCreated.value = true

              video.value.value = ''
              video.value.files = new DataTransfer().files
              videoUrl.value = null
              data.video = null
            })
            .catch(err => { 
              hasError.value = true
              isLoading.value = false
            })
          }
      /**
       * End of Methods
       */
      

      return {
        errors,
        isLoading,
        video,
        isCreated,
        hasError,
        videoUrl,
        videoType,
        setVideo,
        addHighlights
      }
    }
  }
</script>