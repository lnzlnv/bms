<template>
  <div 
    v-if="modalIsOpen"
    class="modal-1 flex items-center"
  >
    <EditForm 
      :selectedAnnouncement="selectedAnnouncement"
      :editSuccess="editSuccess"
    />
  </div>
  <div class="mx-[10vw] relative">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center z-[1000000000000]"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="isLoading"
      class="loading flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div
      v-if="announcementIsDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Announcement has been successfully deleted!
      </div>
    </div>

    <div 
      v-if="announcementIsEdited"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Announcement has been successfully edited!
      </div>
    </div>

    <div class="text-right mb-[1rem]">
      <a href="/announcements/create/">
        <button class="btn-12">
          Add Announcement
        </button>
      </a>
    </div>

    <div 
      v-if="announcements.results && announcements.results.length != 0"
      class="md:grid grid-container-8 gap-[10px]"
    >
      <div 
        v-for="announcement in announcements.results"
        :key="announcement.id"
      >
        <img 
          class="img-15 mx-[auto]"
          :src="typeof announcement.image == 'object'?  windowObj.URL.createObjectURL(announcement.image) : announcement.image"
          alt=""
        >
        <div class="text-1 text-center">
          {{ announcement.date_format_2 }}
        </div>
        
        <div class="grid grid-2-column-2">
          <button
            @click="setSelectedAnnouncement(announcement.id)"
            class="btn-9 mr-[0.5rem] text-center"
          >
            Edit
          </button>
          <button
            @click="deleteAnnouncement(announcement.id)"
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
      No available announcements.
    </p>


    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-if="announcements.previous"
          @click="previous(url)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-if="announcements.next"
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
  import axios from 'axios';  
  import { computed, onBeforeMount, ref, watch, provide } from 'vue';
  import  { page } from '@pages/admin/teams/all/composables.js'
  import EditForm from './EditForm.vue'
  import success from '@composables/generate-account/success.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  
  export default {
    components: {
      EditForm,
      LoadingSpinner
    },
    setup() {
      const announcements = ref({})
      const announcementIsDeleted = success()
      const selectedAnnouncement = ref({})
      const modalIsOpen = ref(false)
      const announcementIsEdited = success()
      const hasError = success()
      const isLoading = ref(false)

      const url = computed(() => {
        return '/api/announcements/'
        + `?limit=${limit}&offset=${limit * pageNumber.value}`
      })

      onBeforeMount(() => {
        getAnnouncements(url.value)
      })

      /**
       * Methods
       */
        const getAnnouncements = (url) => {
          isLoading.value = true
          axios
            .get(url)
            .then(response => {
              announcements.value = response.data
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const deleteAnnouncement = (id) => {
          isLoading.value = true
          const urlDel = '/api/announcements/' + id + '/'

          axios
            .delete(urlDel)
            .then(response => {
              getAnnouncements(url.value)
              announcementIsDeleted.value = true
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        } 

        const setSelectedAnnouncement = (id) => {
          for(let i = 0; i < announcements.value.results.length; ++i) {
            if (announcements.value.results[i].id == id) {
              selectedAnnouncement.value = announcements.value.results[i]
            }
          }
          modalIsOpen.value = true
        }

        const editSuccess = () => {
          announcementIsEdited.value = true
          modalIsOpen.value = false
        }
      /**
       * End of Methods
       */

      provide('hasError', hasError)
      provide('modalIsOpen', modalIsOpen)
      provide('isLoading', isLoading)

      const { pageNumber, limit, next, previous } = page(getAnnouncements)

      return {
        announcements,
        announcementIsDeleted,
        selectedAnnouncement,
        modalIsOpen,
        announcementIsEdited,
        hasError,
        next,
        previous,
        url,
        isLoading,
        getAnnouncements,
        deleteAnnouncement,
        setSelectedAnnouncement,
        editSuccess,
      }
    }
  }
</script>