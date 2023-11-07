<template>
  <div class="container-7">
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
      @submit.prevent="editImage"
      class="relative"
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
        <button class="btn-7 mt-[1rem]">Edit Image</button>
      </div>
    </form>
  </div>
</template>
<script>
  import axios from 'axios';
  import { inject, onBeforeMount, onMounted, reactive, ref } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import success from '@composables/generate-account/success.js'
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import closeIcon from '@images/close-icon.svg'
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';

  export default {
    components: {
      LoadingSpinner,
      Errors,
      DragArea
    },
    setup() {
      const errors = ref({})
      const image = ref(null)
      const data = reactive({
        image: null,
        description: ''
      })
      const isLoading = success()
      const selectedImage = inject('selectedImage', selectedImage)
      const hasError = inject('hasError', hasError)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const isEdited = inject('isEdited', isEdited)
      const imageUrl = ref(null)

      onBeforeMount(() => {
        data.description = selectedImage.value.description
      })
      
      onMounted(() => {
        fileDragAndDrop('js-drag-area', imageUrl, data, 'image')
        
        if (typeof selectedImage.value.image == 'object') {
          let container = new DataTransfer(); 
          container.items.add(selectedImage.value.image)
          image.value.files = container.files
          setDataImage()
          return
        }

        isLoading.value = true
        axios
          .get(selectedImage.value.image, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = selectedImage.value.image_name

            const file = new File(
              [blob], 
              selectedImage.value.image_name, 
              {
                type: blob.type
              }
            )

            let container = new DataTransfer(); 
            container.items.add(file)

            image.value.files = container.files
            setDataImage()
            isLoading.value = false
          })
          .catch(err => {
            hasError.value = true
            isLoading.value = false
          })
      })

      const setDataImage = () => {
        data.image = image.value.files[0]

        if (data.image) {
          imageUrl.value = URL.createObjectURL(data.image)
          return
        }
        
        imageUrl.value = null
      }
      
      const editImage = () => {
        const url = '/api/landing/main-image/'
          + selectedImage.value.id
          + '/'

        isLoading.value = true
        
        axios
          .put(
            url, 
            data,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            for (const key in response.data) {
              selectedImage.value[key] = response.data[key]
            }

            isLoading.value = false
            modalIsOpen.value = false
            isEdited.value = true
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
        data,
        isLoading,
        image,
        selectedImage,
        closeIcon,
        modalIsOpen,
        imageUrl,
        setDataImage,
        editImage
      }
    }
  }
</script>