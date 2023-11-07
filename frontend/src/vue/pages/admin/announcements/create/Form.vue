<template>
  <div class="max-w-[800px] mx-auto pt-0 p-[1em]">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="announcementIsCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Announcement has been successfully created!
      </div>
    </div>

    <form
      @submit.prevent="createAnnouncement"
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

      <div class="mb-[1rem]">
        <input
          v-model="announcement.publish_date"
          class="input-field-3"
          type="datetime-local"
          placeholder="Publish Date"
          required="required"
          title="Publication Date"
        />

        <Errors
          :errors="errors.publish_date"
        />
      </div>

      <div>
        <input 
          @change="getImage"
          class="input-field-3"
          name="image"
          id="image"
          type="file"
          ref="image"
          accept="image/*"
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
          <button class="btn-7 mt-[1rem]">Create Announcement</button>
        </div>
    </form>
  </div>
</template>

<script>
  import host from '@composables/host.js';
  import setCsrfToken from '@composables/csrf-token.js';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import axios from 'axios';
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import success from '@composables/generate-account/success.js'
  import { onMounted, reactive, ref } from 'vue';
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
      const announcement = reactive({
        publish_date: null,
        image: null
      })
      const announcementIsCreated = success()
      const image = ref(null)
      const errors = ref({})
      const isLoading = ref(false)
      const hasError = error()
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop(
          'js-drag-area', 
          imageUrl, 
          announcement, 
          'image',
        )
      })

      const createAnnouncement = () => {
        isLoading.value = true
        const url = host + '/api/announcements/'

        axios
          .post(
            url, 
            announcement,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            announcementIsCreated.value = true
            announcement.image = null
            announcement.publish_date = null

            image.value.value = ''
            image.value.files = new DataTransfer().files
            imageUrl.value = null
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

      const getImage = () => {
        announcement.image = image.value.files[0]

        if (announcement.image) {
          imageUrl.value = URL.createObjectURL(announcement.image)
          return
        }
        
        imageUrl.value = null
      }

      return {
        announcement,
        announcementIsCreated,
        image,
        errors,
        hasError,
        isLoading,
        imageUrl,
        getImage,
        createAnnouncement,
      }
    }
  }
</script>