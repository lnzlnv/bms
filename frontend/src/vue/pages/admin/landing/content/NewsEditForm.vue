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
      @submit.prevent="editNews"
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
        <button class="btn-7 mt-[1rem]">Edit News</button>
      </div>
    </form>
  </div>
</template>
<script>
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import { inject, onMounted, reactive, ref } from 'vue';
  import closeIcon from '@images/close-icon.svg'
  import axios from 'axios';
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
      const isLoading = ref(false)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const selectedNews = inject('selectedNews', selectedNews)
      const hasError = inject('hasError', hasError)
      const isEdited = inject('isEdited', isEdited)
      const data = reactive({
        image: null
      })
      const imageUrl = ref(null)
      

      onMounted(() => {
        fileDragAndDrop('js-drag-area', imageUrl, data, 'image',)

        if (typeof selectedNews.value.image == 'object') {
          let container = new DataTransfer(); 
          container.items.add(selectedNews.value.image)
          image.value.files = container.files
          setImage()
          return
        }

        isLoading.value = true
        axios
          .get(selectedNews.value.image, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = selectedNews.value.image_name

            const file = new File(
              [blob], 
              selectedNews.value.image_name, 
              {
                type: blob.type
              }
            )

            let container = new DataTransfer(); 
            container.items.add(file)

            image.value.files = container.files
            setImage()
            isLoading.value = false
          })
          .catch(err => {
            console.log(err)
            hasError.value = true
            isLoading.value = false
          })
      })

      const editNews = () => {
        isLoading.value = true
        const url = '/api/landing/news/'
          + selectedNews.value.id
          + '/'

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
              selectedNews.value[key] = response.data[key]
            }

            isLoading.value = false
            modalIsOpen.value = false
            isEdited.value = true
          })
          .catch(err => {
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
        errors,
        isLoading,
        closeIcon,
        modalIsOpen,
        image,
        imageUrl,
        editNews,
        setImage
      }
    }
  }
</script>