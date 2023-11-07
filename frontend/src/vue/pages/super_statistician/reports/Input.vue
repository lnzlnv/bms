<template>
  <input 
    :class="class"
    type="number"
    :name="name"
    :value="value"
    @focusout="updateStat($event, value, statId, playerNumber)"
    :disabled="game.is_approved_by_admin"
  >
</template>

<script>
import { inject } from 'vue';

  export default {
    props: {
      name: String,
      value: Number,
      statId: Number,
      class: {
        type: String,
        default: 'input-field-6'
      },
      disabled: {
        type: Boolean,
      },
      playerNumber: {
        type: Number,
        default: null
      }
    },
    setup(props) {
      const updateStat = inject('updateStat', updateStat)
      const game = inject('game', game)

      return {
        ...props,
        updateStat,
        game,
      }
    }
  }
</script>