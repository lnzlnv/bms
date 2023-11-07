<template>
  <div class="mx-[10vw] mb-[2rem]">
    <div 
      v-if="isLoading"
      class="loading flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div 
      v-if="hasError"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="isDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        <span v-show="activeTab == 1">Main Image</span>
        <span v-show="activeTab == 2">Highlights</span>
        <span v-show="activeTab == 3">News</span>
        has been successfully deleted!
      </div>
    </div>

    <div 
      v-if="isEdited"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        <span v-show="activeTab == 1">Main Image</span>
        <span v-show="activeTab == 2">Highlights</span>
        <span v-show="activeTab == 3">News</span>
        has been successfully edited!
      </div>
    </div>
    
    <div
      v-if="modalIsOpen"
      class="modal-1 flex items-center"
    >
      <MainEditForm v-if="activeTab == 1" />
      <HighlightsEditForm v-if="activeTab == 2" />
      <NewsEditForm v-if="activeTab == 3" />
    </div>


    <div class="flex flex-col-reverse md:flex-row md:items-center md:justify-between">
      <TabButtons />
      <CreateButtons />
      <TabDropdown />
    </div>

    <div>
      <TableMain v-show="activeTab == 1" />
      <TableHighlights v-show="activeTab == 2" />
      <TableNews v-show="activeTab == 3" />
    </div>
  </div>
</template>
<script>
  import { provide, ref } from 'vue';
  import success from '@composables/generate-account/success.js'  
  import TabButtons from './TabButtons.vue';
  import CreateButtons from './CreateButtons.vue';
  import TabDropdown from './TabDropdown.vue'
  import TableMain from './TableMain.vue';
  import setCsrfToken from '@composables/csrf-token.js';
  import MainEditForm from './MainEditForm.vue';
  import TableHighlights from './TableHighlights.vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import HighlightsEditForm from './HighlightsEditForm.vue';
  import TableNews from './TableNews.vue';
  import NewsEditForm from './NewsEditForm.vue';

  setCsrfToken()

  export default {
    components: {
      TabButtons,
      CreateButtons,
      TabDropdown,
      TableMain,
      MainEditForm,
      TableHighlights,
      LoadingSpinner,
      HighlightsEditForm,
      TableNews,
      NewsEditForm
    },
    setup() {
      const activeTab = ref(1)
      const hasError = success()
      const isDeleted = success()
      const isEdited = success()
      const modalIsOpen = ref(false)
      const selectedImage = ref({})
      const selectedHighlight = ref({})
      const selectedNews = ref({})
      const isLoading = ref(false)

      provide('activeTab', activeTab)
      provide('hasError', hasError)
      provide('isDeleted', isDeleted)
      provide('isEdited', isEdited)
      provide('modalIsOpen', modalIsOpen)
      provide('selectedImage', selectedImage)
      provide('isLoading', isLoading)
      provide('selectedHighlight', selectedHighlight)
      provide('selectedNews', selectedNews)

      return {
        activeTab,
        isDeleted,
        hasError,
        modalIsOpen,
        isEdited,
        isLoading
      }
    }
  }
</script>