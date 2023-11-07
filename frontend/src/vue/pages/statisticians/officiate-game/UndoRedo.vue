<template>
  <div>
    <button 
      @click="changeHistory('UNDO')"
      class="mr-[0.5rem]"
    >
      <img  
        class="img-14 rotate-2"
        :src="undo" 
        alt=""
        title="Undo"
      >
    </button>
  </div>
</template>
<script>
  import undo from '@images/undo.svg'
  import { inject } from 'vue';

  export default {
    setup() {
      const socket = inject('socket', socket)
      const game = inject('game', game)
      const roomMemberUniqueID = inject('roomMemberUniqueID', roomMemberUniqueID)
      const isLoading = inject('isLoading', isLoading)

      const changeHistory = (operation) => {
        const data = {
          type: 'history',
          operation: operation,
          statistician: game.value.statistician.id,
          game_id: game.value.id,
          room_member_id: roomMemberUniqueID,
          message: {
            class: 'success-1',
            content: operation.charAt(0).toUpperCase() 
              + operation.slice(1).toLowerCase() 
              + ' is successfull!'
          }
        }

        isLoading.value = true
        socket.value.send(JSON.stringify(data))
      }

      return {
        undo,
        changeHistory
      }
    }
  }
</script>