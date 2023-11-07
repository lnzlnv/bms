<template>
  <div 
    v-if="modalIsOpen"
    class="modal-1 flex items-center"
  >
    <EditForm 
      :options="options"
      :selectedBanner="selectedBanner"
      :banners="banners"
      :season="season"
      :division="division"
      :editSuccess="editSuccess"
    />
  </div>

  <div 
    v-if="isLoading"
    class="loading-2 flex justify-center"
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

  <div
    v-if="bannerIsDeleted"
    class="container-6 flex justify-center"
  >
    <div class="delete-1">
      Schedule Banner has been successfully deleted!
    </div>
  </div>

  <div 
    v-if="bannerIsEdited"
    class="container-6 flex justify-center"
  >
    <div class="success-1">
      Schedule Banner has been successfully edited!
    </div>
  </div>

  <div class="mx-[10vw] mb-[4rem]">
    <div class="md:grid grid-2-column-2 md:mb-[1rem]">
      <div class="mb-[1rem] md:mb-0">
        <a href="/schedules/banner/create/">
          <button class="btn-12">Add Banner</button>
        </a>
      </div>
      <form class="mb-[1rem] md:mb-0 md:flex justify-end items-center gap-[20px]">
        <div class="grid grid-2-column-3 items-center mb-[1rem] md:mb-0">
          <select
            v-model="season"
            class="input-field-5"
            name="season"
            id="season"
          >
            <option value="" disabled selected>Select Season</option>
            <option
              v-for="season in options.seasons"
              :key="season.id"
              :value="season.id"
            >
              {{ season.year }}
            </option>
          </select>
        </div>
        <div class="grid grid-2-column-3">
          <select
            v-model="division"
            class="input-field-5"
            name="division"
            id="division"
          >
            <option value="" disabled selected>Select Division</option>
            <option
              v-for="division in options.divisions"
              :key="division[0]"
              :value="division[0]"
            >
              {{ division[1] }}
            </option>
          </select>
        </div>
      </form>
    </div>

    <div 
        v-if="banners.results && banners.results.length != 0"
        class="md:grid grid-container-8 gap-[10px]"
      >
        <div 
          v-for="banner in banners.results"
          :key="banner.id"
        >
          <img 
            class="img-15 mx-[auto]"
            :src="typeof banner.image == 'object'?  windowObj.URL.createObjectURL(banner.image) : banner.image"
            alt=""
          >
          <div class="text-1 text-center">
            {{ banner.date_format }}
          </div>
          
          <div class="grid grid-2-column-2">
            <button
              @click="editBanner(banner.id)"
              class="btn-9 mr-[0.5rem] text-center"
            >
              Edit
            </button>
            <button
              @click="deleteBanner(banner.id)"
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
        No available banner.
      </p>

    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-if="banners.previous"
          @click="previous(bannersUrl)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-if="banners.next"
          @click="next(bannersUrl)"
          class="btn-11"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { onBeforeMount, ref, watch, provide, computed } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import host from '@composables/host.js';
  import normalizeData from '@composables/normalize-data.js'
  import setCsrfToken from '@composables/csrf-token.js';
  import  { page } from '@pages/admin/teams/all/composables.js'
  import EditForm from './EditForm.vue';
  import success from '@composables/generate-account/success.js'

  setCsrfToken()

  export default {
    components: {
      EditForm,
      LoadingSpinner
    },
    setup() {
      const options = ref({})
      const season = ref(0)
      const division = ref('J')
      const banners = ref({})
      const isLoading = ref(false)
      const modalIsOpen = ref(false)
      const selectedBanner = ref({})
      const windowObj = ref(window);
      const bannerIsDeleted = success()
      const bannerIsEdited = success()
      const hasError = success()

      onBeforeMount(() => {
        isLoading.value = true
        const url = host + '/api/game-schedule/banner/options/'

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            season.value = response.data.current_season.id
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      /**
       * Methods
       */
        const getBanners = () => {
          isLoading.value = true
          axios
            .get(bannersUrl.value)
            .then(response => {
              banners.value = response.data
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const deleteBanner = (id) => {
          isLoading.value = true
          const url = host + '/api/game-schedule/banner/' + id + '/'
          
          axios
            .delete(url)
            .then(response => {
              bannerIsDeleted.value = true
              getBanners(bannersUrl)
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const getPage = (url) => {
          isLoading.value = true
          axios
            .get(url)
            .then(response => {
              banners.value = normalizeData(response.data)
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const editSuccess = () => {
          bannerIsEdited.value = true
        }

        const editBanner = (id) => {
          modalIsOpen.value = true
          selectedBanner.value = banners.value.results[id]

          for(let i = 0; i < banners.value.results.length; ++i) {
            if (banners.value.results[i].id == id) {
              selectedBanner.value = banners.value.results[i]
            }
          }
        }
      /**
       * End of Methods
       */

      /**
       * Computed
       */
        const bannersUrl = computed(() => {
          return host 
            + '/api/game-schedule/banner/' 
            + season.value 
            + '/' 
            + division.value 
            + '/'
            + `?limit=${limit}&offset=${limit*pageNumber.value}`
        })
      /**
       * End of Computed
       */

      /**
       * Watch
       */
        watch(
          [season, division],
          () => {
            pageNumber.value = 0
            getBanners()
          }
        )
      /**
       * End of Watch
       */

      provide('hasError', hasError)
      provide('modalIsOpen', modalIsOpen)

      const { pageNumber, limit, next, previous } = page(getPage)

      return {
        options,
        season,
        division,
        banners,
        bannerIsDeleted,
        modalIsOpen,
        selectedBanner,
        windowObj,
        bannerIsEdited,
        hasError,
        next,
        previous,
        bannersUrl,
        isLoading,
        deleteBanner,
        editBanner,
        getPage,
        editSuccess,
      }
    }
  }
</script>