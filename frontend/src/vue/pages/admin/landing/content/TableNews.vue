<template>
  <div>
    <div 
      v-if="images.results && images.results.length != 0"
      class="lg:grid grid-container-8 gap-[10px]"
    >
      <div
        v-for="news in images.results"
        :key="news.id"
      >
        <img 
          class="img-13 mb-[1rem]"
          :src="news.image" 
          alt=""
        >
        <div class="grid grid-2-column-2 gap-[10px]">
          <button
            @click="selectNews(news.id)"
            class="btn-9"
          >
            Edit
          </button>
          <button
            @click="deleteNews(news.id)"
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
      No available news.
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
      const mainUrl = '/api/landing/news/'
      const hasError = inject('hasError', hasError)
      const isLoading = inject('isLoading', isLoading)
      const isDeleted = inject('isDeleted', isDeleted)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const selectedNews = inject('selectedNews', selectedNews)

      onBeforeMount(() => {
        getNews(mainUrl)
      })

      /**
       * Computed
       */
        const url = computed(() => {
          return mainUrl
            + `?limit=${limit}&${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */

      /**
        * Methods
        */
        const getNews = (url) => {
          axios
            .get(url)
            .then(response => {
              images.value = response.data
            })
            .catch(err => {
              hasError.value = true
            })
        }

        const deleteNews = (id) => {
          isLoading.value = true
          const url = mainUrl
            + id
            + '/'
          
          axios
            .delete(url)
            .then(response => {
              getNews(url)
              isLoading.value = false
              isDeleted.value = true
            })
            .catch(err => {
              hasError.value = true
              isLoading.value = false
            })
        }

        const selectNews = (id) => {
          selectedNews.value = images.value.results.filter(news => 
            news.id == id
          )[0]
          modalIsOpen.value = true
        }
      /**
       * End of Methods
       */

      const { pageNumber, limit, next, previous } = page(getNews)

      return {
        next,
        previous,
        images,
        url,
        modalIsOpen,
        deleteNews,
        selectNews
      }
    }
  }
</script>