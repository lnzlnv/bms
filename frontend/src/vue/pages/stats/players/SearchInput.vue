<template>
  <div class="text-right">
    <div class="flex justify-end">
      <input
        class="input-field-2"
        type="search"
        name="search"
        id="search"
        placeholder="Search"
      />

      <button class="btn-5">
        <img 
          class="icon-1"
          :src="icon_search" 
          alt="search icon" 
        />
      </button>
    </div>
  </div>
</template>

<script>
  import icon_search from '@images/icon-search.png'

  export default {
    setup() {
      return {
        icon_search
      }
    }
  }
</script>