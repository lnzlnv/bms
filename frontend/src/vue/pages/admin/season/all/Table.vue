<template>
  <div>
    <div
      v-if="modalIsOpen"
      class="modal-1 flex items-center"
    >
      <EditForm
        :selectedSeason="selectedSeason"
        :editSuccess="editSuccess"
      />
    </div>

    <div 
      v-if="isLoading"
      class="loading flex justify-center"
    >
      <LoadingSpinner />
    </div>
    
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div class="mx-[10vw] mb-[4rem]">
      <div 
        v-if="seasonIsEdited"
        class="container-6 flex justify-center"
      >
        <div class="success-1">
          Season has been successfully edited!
        </div>
      </div>

      <div
        v-if="seasonIsDeleted"
        class="container-6 flex justify-center"
      >
        <div class="delete-1">
          Season has been successfully deleted!
        </div>
      </div>

      <div class="text-right mb-[1rem]">
        <a href="/seasons/create/">
          <button class="btn-12">Add Season</button>
        </a>
      </div>

      <div 
        v-if="seasons.results && seasons.results.length != 0"
        class="md:grid grid-container-8 gap-[10px]"
      >
        <div 
          v-for="season in seasons.results"
          :key="season.id"
        >
          <img 
            class="img-15 mx-[auto]"
            :src="typeof season.logo == 'object'?  windowObj.URL.createObjectURL(season.logo) : season.logo"
            alt=""
          >
          <div class="text-1 text-center">
            {{ season.year }}
          </div>
          
          <div class="grid grid-2-column-2">
            <button
              @click="selectedSeasonToEdit(season.id)"
              class="btn-9 mr-[0.5rem] text-center"
            >
              Edit
            </button>
            <button
              @click="deleteSeason(season.id)"
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
        No available seasons.
      </p>

      <div class="text-center mt-[2rem]">
        <div>
          <button
            v-if="seasons.previous"
            @click="previous(seasonsUrl)"
            class="btn-11 mr-[0.5rem]"
          >
            Prev
          </button>
          <button
            v-if="seasons.next"
            @click="next(seasonsUrl)"
            class="btn-11"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { computed, onBeforeMount, ref, provide } from 'vue';
  import setCsrfToken from '@composables/csrf-token.js';
  import host from '@composables/host.js';
  import  { page } from '@pages/admin/teams/all/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import EditForm from './EditForm.vue';
  import success from '@composables/generate-account/success.js'

  setCsrfToken()

  export default {
    components: {
      EditForm,
      LoadingSpinner
    },    
    setup() {
      const seasons = ref({})
      const isLoading = ref(false)
      const windowObj = ref(window)
      const selectedSeason = ref({})
      const modalIsOpen = ref(false)
      const seasonIsEdited = success()
      const seasonIsDeleted = success()
      const hasError = success()

      onBeforeMount(() => {
        getSeasons(seasonsUrl.value)
      })

      /**
       * Computed
       */
        const seasonsUrl = computed(() => {
          return host 
            + '/api/seasons/'
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */
      
      /**
       * Methods
       */
        const getSeasons = (url) => {
          isLoading.value = true
          axios
            .get(url)
            .then(response => {
              seasons.value = response.data
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const deleteSeason = (id) => {
          isLoading.value = true
          const url = '/api/seasons/' + id + '/'

          axios
            .delete(url)
            .then(response => {
              seasonIsDeleted.value = true
              getSeasons(seasonsUrl.value)
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const selectedSeasonToEdit = (id) => {
          for(let i = 0; i < seasons.value.results.length; ++i) {
            if (seasons.value.results[i].id == id) {
              selectedSeason.value = seasons.value.results[i]
            }
          }
          modalIsOpen.value = true
        }

        const editSuccess = () => {
          seasonIsEdited.value = true
          modalIsOpen.value = false
        }
      /**
       * End of Methods
       */

      provide('hasError', hasError)
      provide('modalIsOpen', modalIsOpen)

      const { pageNumber, limit, next, previous } = page(getSeasons)

      return {
        seasons,
        seasonIsDeleted,
        seasonIsEdited,
        selectedSeason,
        modalIsOpen,
        windowObj,
        hasError,
        next,
        previous,
        seasonsUrl,
        isLoading,
        deleteSeason,
        getSeasons,
        selectedSeasonToEdit,
        editSuccess,
      }
    }
  }
</script>