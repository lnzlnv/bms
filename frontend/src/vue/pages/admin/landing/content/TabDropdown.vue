<template lang="">
  <div class="mb-[1rem] md:hidden">
    <select 
      v-model="activeTab"
      class="input-field-3"
    >
      <option value="1">Main</option>
      <option value="2">Highlights</option>
      <option value="3">News</option>
    </select>
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