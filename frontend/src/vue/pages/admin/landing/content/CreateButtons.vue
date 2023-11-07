<template lang="">
  <div class="mb-[1rem]">
    <a
      v-show="activeTab == 1"
      class="btn-12" 
      href="/administration/landing/main/add-image/"
    >
      Add Image
    </a>
    <a
      v-show="activeTab == 2"
      class="btn-12" 
      href="/administration/landing/highlights/add-video/"
    >
      Add Highlights
    </a>
    <a
      v-show="activeTab == 3"
      class="btn-12" 
      href="/administration/landing/news/add-image/"
    >
      Add News
    </a>
  </div>
</template>
<script>
  import { inject } from 'vue';

  export default {
    setup() {
      const activeTab = inject('activeTab', activeTab)

      return {
        activeTab
      }
    }
  }
</script>