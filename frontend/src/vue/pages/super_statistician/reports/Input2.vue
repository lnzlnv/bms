<template>
  <input 
    :class="class"
    type="number"
    :name="name"
    :value="value"
    @focusout="updateStatType($event, value, classificationId, type)"
    :disabled="game.is_approved_by_admin"
  >
</template>

<script>
import { inject } from 'vue';

  export default {
    props: {
      name: String,
      value: Number,
      classificationId: Number,
      class: {
        type: String,
        default: 'input-field-6'
      },
      type: String
    },
    setup(props) {
      const updateStatType = inject('updateStatType', updateStatType)
      const game = inject('game', game)

      return {
        ...props,
        updateStatType,
        game
      }
    }
  }
</script>