<template>
  <div class="md:hidden mb-[2rem]">
    <select
      @change="activeTabChange"
      v-model="activeTab"
      class="input-field-3"
    >
      <option value="1">Home</option>
      <option value="2">Away</option>
      <option value="3">Half-Time Analysis</option>
      <option value="4">Full-Time Analysis</option>
    </select>
  </div>
</template>

<script>
import { inject, watch } from 'vue';

  export default {
    setup() {
      const activeTab = inject('activeTab', activeTab)
      const changeActiveTab = inject('changeActiveTab', changeActiveTab)
      
      const activeTabChange = () => {
        changeActiveTab(activeTab.value)
      }

      return {
        activeTab,
        changeActiveTab,
        activeTabChange
      } 
    }
  }
</script>