<template>
  <div class="mx-[10vw] mb-[2rem]">
    <div 
      v-if="isLoading"
      class="loading flex justify-center"
    >
      <LoadingSpinner />
    </div>

    <div 
      v-if="hasError"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>


    <div
      v-if="isDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Account has been successfully deleted!
      </div>
    </div>

    <div 
        v-if="emailSent"
        class="container-6 flex justify-center"
      >
        <div class="success-1">
          Email has been successfully sent!
        </div>
      </div>

    <div class="flex flex-col-reverse mb-[1rem] md:flex-row md:items-center md:justify-between">
      <div class="grid grid-2-column-2">
        <button 
          @click="activeTab = 1"
          :class="activeTab == 1? 'active': ''"
          class="btn-21"
        >
          Accounts
        </button>

        <div class="relative">
          <button 
            @click="activeTab = 2"
            class="btn-21 w-full"
            :class="activeTab == 2? 'active': ''"
          >
            Requests
          </button>

          <div 
            v-show="requestsCount > 0"
            class="notification-count pos-item-5 flex justify-center items-center"
          >
            {{ requestsCount }}
          </div>
        </div>
      </div>

      <a
        class="btn-12 mb-[1rem] md:mb-0"
        href="/administration/generate-account/"
      >
        Generate Account
      </a>
    </div>

    <AccountsTable v-show="activeTab == 1" />
    <ActivationRequestTable v-show="activeTab == 2" />
  </div>
</template>

<script>
  import { provide, ref } from 'vue';
  import { error } from '@pages/admin/teams/create/composables.js'
  import deleted from '@composables/generate-account/is-deleted.js'
  import setCsrfToken from '@composables/csrf-token.js';
  import success from '@composables/generate-account/success.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import AccountsTable from './AccountsTable.vue'
  import ActivationRequestTable from './ActivationRequestTable.vue';

  setCsrfToken()

  export default {
    components: {
      LoadingSpinner,
      AccountsTable,
      ActivationRequestTable
    },
    setup() {
      const hasError = error()
      const { isDeleted } = deleted()
      const emailSent = success()
      const isLoading = ref(false)
      const activeTab = ref(1)
      const requestsCount = ref(0)

      provide('hasError', hasError)
      provide('isLoading', isLoading)
      provide('emailSent', emailSent)
      provide('requestsCount', requestsCount)

      return {
        hasError,
        isDeleted,
        emailSent,
        isLoading,
        activeTab,
        requestsCount
      }
    }
  }
</script>