<template>
  <div class="max-w-[800px] mx-auto px-[1em] mb-[4rem] relative">
    <div 
      v-if="isCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        News has been successfully added!
      </div>
    </div>

    <form
      @submit.prevent="addNews"
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
          @change="setImage"
          ref="image"
          class="input-field-3"
          type="file" 
          name="news" 
          id="news"
          accept="image/*"
          hidden="hidden"
        >

        <DragArea 
          forInput="news"
          dragAreaName="js-drag-area"
          :imageUrl="imageUrl"
        />

        <Errors 
          :errors="errors.image"
        />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Add News</button>
      </div>
    </form>
  </div>
</template>
<script>
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import { onMounted, reactive, ref } from 'vue';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import axios from 'axios';
  import success from '@composables/generate-account/success.js'
  import setCsrfToken from '@composables/csrf-token.js';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';

  setCsrfToken()

  export default {
    components: {
      LoadingSpinner,
      Errors,
      DragArea
    },
    setup() {
      const isLoading = ref(false)
      const image = ref(null)
      const errors = ref({})
      const hasError = success()
      const isCreated = success()
      const data = reactive({
        image: null
      })
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop('js-drag-area', imageUrl, data, 'image')
      })

      const addNews = () => {
        isLoading.value = true
        const url = '/api/landing/news/'

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
            image.value.value = ''
            image.value.files = new DataTransfer().files
            imageUrl.value = null
            data.image = null
            isLoading.value = false
            isCreated.value = true
          })
          .catch(err => {
            isLoading.value = false
            if (err.response.status != 400) {
              hasError.value = true
              return
            }
            
            errors.value = err.response.data
          })
      }

      const setImage = () => {
        data.image = image.value.files[0]

        if (data.image) {
          imageUrl.value = URL.createObjectURL(data.image)
          return
        }
        
        imageUrl.value = null
      }

      return {
        isLoading,
        image,
        errors,
        isCreated,
        imageUrl,
        setImage,
        addNews
      }
    }
  }
</script>