<template>
  <div class="container-7">
    <div class="text-right mb-[1rem]">
      <button
        @click="modalIsOpen = false"
      >
        <img 
        class="icon-2"
        :src="closeIcon" 
        alt="close icon"
      />
      </button>
    </div>

    <form @submit.prevent="activateAccount(userData, 1)">
      <div>
        <input 
          v-model="userData.expiration_date"
          class="input-field-3"
          type="datetime-local" 
          name="expiration_date" 
          id="expiration_date"
          title="Expiration Date"
          required="required"
        >
        <Errors
          :errors="errors.expiration_date"
        />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Activate</button>
      </div>
    </form>
  </div>
</template>

<script>
  import { inject } from 'vue'
  import closeIcon from '@images/close-icon.svg'
  import Errors from '@pages/admin/schedules/create/Errors.vue';

  export default {
    components: {
      Errors
    },
    setup() {
      const userData = {
        expiration_date: null
      }
      const hasError = inject('hasError', hasError)
      const isLoading = inject('isLoading', isLoading)
      const selectedPlayer = inject('selectedPlayer', selectedPlayer)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const activateAccount = inject('activateAccount', activateAccount)
      const errors = inject('errors', errors)

      return {
        userData,
        activateAccount,
        modalIsOpen,
        closeIcon,
        errors
      }
    }
  }
</script>