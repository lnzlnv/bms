<template>
  <div>
    <div 
      v-if="highlights.results && highlights.results.length > 0"
      class="lg:grid grid-container-8 gap-[10px]"
    >
      <div
        v-for="highlight in highlights.results"
        :key="highlight.id"
      >
        <video
          class="mb-[1rem]"
          controls
        >
          <source 
            :src="highlight.video" 
            :type="highlight.video_type"
          >
          Your browser does not support the video tag.
        </video>
        
        <div class="grid grid-2-column-2 gap-[10px]">
          <button
            @click="selectHighlight(highlight.id)"
            class="btn-9"
          >
            Edit
          </button>
          <button
            @click="deleteHighlights(highlight.id)"
            class="btn-10"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    <p 
      v-else 
      class="text-1 text-center"
    >
      No available highlights.
    </p>

    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-show="highlights.previous"
          @click="previous(url)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-show="highlights.next"
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
  import axios from 'axios'
  import { computed, inject, onBeforeMount, ref } from 'vue'
  import  { page } from '@pages/admin/teams/all/composables.js'

  export default {
    setup() {
      const highlights = ref({})
      const hasError = inject('hasError', hasError)
      const isLoading = inject('isLoading', isLoading)
      const isDeleted = inject('isDeleted', isDeleted)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const selectedHighlight = inject('selectedHighlight', selectedHighlight)
      const mainUrl = '/api/landing/highlights/'

      onBeforeMount(() => {
        getHighlights(mainUrl)
      })

      /**
       * Computed
       */
        const url = computed(() => {
          return mainUrl
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */

      /**
       * Methods
       */
        const getHighlights = (url) => {
          axios
            .get(url)
            .then(response => {
              highlights.value = response.data
            })
            .catch(err => {
              hasError.value = true
            })
        }

        const deleteHighlights = (id) => {
          isLoading.value = true
          const deleteUrl = mainUrl
            + id
            + '/'

          axios
            .delete(deleteUrl)
            .then(response => {
              getHighlights(url.value)
              isLoading.value = false
              isDeleted.value = true
            })
            .catch(err => {
              hasError.value = true
              isLoading.value = false
            })
        }

        const selectHighlight = (id) => {
          selectedHighlight.value = highlights.value.results.filter(
            highlight => highlight.id == id
          )[0]
          modalIsOpen.value = true
        }
      /**
       * End of Methods
       */
      
      const { pageNumber, limit, next, previous } = page(getHighlights)

      return {
        highlights,
        next,
        previous,
        url,
        modalIsOpen,
        deleteHighlights,
        selectHighlight
      }
    }
  }
</script>