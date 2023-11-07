<template>
  <div>
    <div 
      v-if="images.results && images.results.length != 0"
      class="md:grid grid-container-8 gap-[10px]"
    >
      <div
        v-for="image in images.results"
        :key="image.id"
        class="mb-[1rem] lg:mb-0"
      >
        <div>
          <img 
            class="img-15 mx-[auto]"
            :src="image.image" 
          >
          <p class="text-1 text-center">
            {{ image.desc_1 }}
          </p>
        </div>
        
        <div class="grid grid-2-column-2 gap-[10px]">
          <button
            @click="selectImage(image.id)"
            class="btn-9"
          >
            Edit
          </button>
          <button
            @click="deleteImage(image.id)"
            class="btn-10"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    <p v-else class="text-1 text-center">
      No available images.
    </p>
    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-show="images.previous"
          @click="previous(url)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-show="images.next"
          @click="next(url)"
          class="btn-11"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
<script>
  import { computed, inject, onBeforeMount, ref } from 'vue';
  import  { page } from '@pages/admin/teams/all/composables.js'
  import axios from 'axios';

  export default {
    setup() {
      const images = ref({})
      const selectedImage = inject('selectedImage', selectedImage)
      const hasError = inject('hasError', hasError)
      const isDeleted = inject('isDeleted', isDeleted)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const isLoading = inject('isLoading', isLoading)

      onBeforeMount(() => {
        getImages(url.value)
      })

      /**
       * Computed
       */
        const url = computed(() => {
          return '/api/landing/main-image/'
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */

      /**
       * Methods
       */
        const getImages = (url) => {
          isLoading.value = true
          axios
          .get(url)
          .then(response => {
            images.value = response.data
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
        }

        const deleteImage = (id) => {
          isLoading.value = true
          const deleteUrl = '/api/landing/main-image/'
            + id
            + '/'
          
          axios
            .delete(deleteUrl)
            .then(response => {
              getImages(url.value)
              isDeleted.value = true
              isLoading.value = false
            })
            .catch(err => {
              hasError.value = true
              isLoading.value = false
            })
        } 

        const selectImage = (id) => {
          selectedImage.value = images.value.results.filter(image => 
            image.id == id
          )[0]
          modalIsOpen.value = true
        }
      /**
       * End of Methods
       */

      const { pageNumber, limit, next, previous } = page(getImages)

      return {
        images,
        url,
        next,
        previous,
        modalIsOpen,
        deleteImage,
        selectImage
      }
    }
  }
</script>