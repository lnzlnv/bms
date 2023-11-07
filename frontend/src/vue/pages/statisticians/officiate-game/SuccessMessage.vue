<template>
  <div class="success-message flex flex-col items-center">
    <div 
      v-for="message in messages"
      :key="message"
      :class="message.class"
      class="mb-[1rem] flex"
    >
      {{ message.content }}
    </div>
  </div>
</template>

<script>
import { inject } from 'vue';

  export default {
    setup() {
      const messages = inject('messages', messages)

      return {
        messages
      }
    }
  }
</script>