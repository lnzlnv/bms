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
        Main Image has been successfully added!
      </div>
    </div>

    <form
      @submit.prevent="addImage"
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
          v-model="data.description"
          class="input-field-3"
          type="text" 
          name="description" 
          id="description"
          placeholder="Description"
          required="required"
        >

        <Errors 
          :errors="errors.description"
        />
      </div>

      <div class="mb-[1rem]">
        <input
          @change="setDataImage"
          ref="image"
          class="input-field-3" 
          type="file" 
          name="image" 
          id="image"
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
        <button class="btn-7 mt-[1rem]">Add Image</button>
      </div>
    </form>
  </div>
</template>
<script>
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import axios from 'axios';
  import { onMounted, reactive, ref } from 'vue';
  import success from '@composables/generate-account/success.js'
  import setCsrfToken from '@composables/csrf-token.js';
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
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
      const errors = ref({})
      const data = reactive({
        description: '',
        image: null
      })
      const image = ref(null)
      const isCreated = success()
      const hasError = success()
      const isLoading = success()
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop('js-drag-area', imageUrl, data, 'image')
      })

      const setDataImage = () => {
        data.image = image.value.files[0]

        if (data.image) {
          imageUrl.value = URL.createObjectURL(data.image)
          return
        }
        
        imageUrl.value = null
      }

      const addImage = () => {
        isLoading.value = true

        const url = '/api/landing/main-image/'
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
          isCreated.value = true
          data.image = null
          data.description = ''

          image.value.value = ''
          image.value.files = new DataTransfer().files
          imageUrl.value = null
          isLoading.value = false
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
      
      return {
        errors,
        image,
        data,
        isCreated,
        hasError,
        isLoading,
        imageUrl,
        setDataImage,
        addImage
      }
    }
  }
</script>