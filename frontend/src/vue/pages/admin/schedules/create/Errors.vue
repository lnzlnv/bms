<template>
  <ul>
    <li class="error-1" v-for="error in errors" :key="error">
      {{ error }}
    </li>
  </ul>
</template>

<script>
  export default {
    props: ['errors']
  }
</script>