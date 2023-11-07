<template lang="">
  <div class="mb-[1rem] hidden md:block">
    <button 
      :class="activeTab == 1? 'active': ''"
      @click="activeTab = 1"
      class="btn-21"
    >
      Main
    </button>
    <button
      :class="activeTab == 2? 'active': ''"
      @click="activeTab = 2"
      class="btn-21"
    >
      Highlights
    </button>
    <button
      :class="activeTab == 3? 'active': ''"
      @click="activeTab = 3"
      class="btn-21"
    >
      News
    </button>
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