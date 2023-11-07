<template>
  <div>
    <div 
    v-if="isApproved"
    class="container-6 flex justify-center"
  >
    <div class="success-1">
      Account activation request been successfully approved!
    </div>
  </div>

  <div
      v-if="isDeleted"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        Account activation request been successfully rejected!
      </div>
    </div>

    <div 
      v-show="modalIsOpen"
      class="modal-1 flex items-center"
    >
      <Form />
    </div>

    <table class="table-1">
      <thead>
        <tr>
          <th class="table-1__header text-left">Username</th>
          <th class="table-1__header text-left">First Name</th>
          <th class="table-1__header text-left">Last Name</th>
          <th class="table-1__header text-left">Email</th>
          <th class="table-1__header text-left">User Role</th>
          <th class="table-1__header text-left"></th>
        </tr>
      </thead>
      <tbody v-if="accounts.results && accounts.results.length != 0">
        <tr
          v-for="account in accounts.results"
          :key="account.id"
          class="table-1__row flex flex-col lg:table-row"
        >
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Username"
          >
            {{ account.username }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="First Name"
          >
            {{ account.first_name }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Last Name"
          >
            {{ account.last_name }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="Email"
          >
            {{ account.email }}
          </td>
          <td
            class="table-1__data text-left lg:table-cell"
            data-cell="User Role"
          >
            {{ account.user_role_name }}
          </td>
          <td
            class="table-1__data empty text-left lg:table-cell"
          >
            <div class="grid grid-2-column-2 gap-[10px]">
              <button
                @click="selectedPlayer = account.id; modalIsOpen = true"
                class="btn-9"
              >
                Approve
              </button>
              <button
                @click="selectedPlayer = account.id; activateAccount({}, 0)"
                class="btn-10"
              >
                Reject
              </button>
            </div>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr class="table-1__row flex flex-col lg:table-row">
          <td 
            class="table-1__data empty lg:table-cell"
            colspan="6"
          >
            No account activation request available.
          </td>
        </tr>
      </tbody>
    </table>
    <div class="text-center mt-[2rem]">
      <div>
        <button
          v-if="accounts.previous"
          @click="previous(url)"
          class="btn-11 mr-[0.5rem]"
        >
          Prev
        </button>
        <button
          v-if="accounts.next"
          @click="next(url)"
          class="btn-11"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { computed, inject, onBeforeMount, provide, ref } from 'vue';
  import  { page } from '@pages/admin/teams/all/composables.js'
  import Form from './Form.vue'
  import success from '@composables/generate-account/success.js'
  import deleted from '@composables/generate-account/is-deleted.js'

  export default {
    components: {
      Form
    },
    setup() {
      const accounts = ref({})
      const selectedPlayer = ref()
      const errors = ref({})
      const modalIsOpen = ref(false)
      const isLoading = inject('isLoading', isLoading)
      const hasError = inject('hasError', hasError)
      const requestsCount = inject('requestsCount', requestsCount)
      const isApproved = success()
      const { isDeleted } = deleted()

      onBeforeMount(() => {
        getAccounts(url.value)
      })

      /**
       * Computed
       */
        const url = computed(() => {
          return '/api/account/generate/activation-requests/'
            + `?limit=${limit}&offset=${limit * pageNumber.value}`
        })
      /**
       * End of Computed
       */

      /**
       * Methods
       */
        const getAccounts = (url) => {
          isLoading.value = true

          axios
          .get(url)
          .then(response => {
            accounts.value = response.data
            isLoading.value = false
            requestsCount.value = accounts.value.results.length
          })
          .catch(err => {
            hasError.value = true
            isLoading.value = false
          })
        }

        const activateAccount = (data={}, approved) => {
          const url1 = '/api/account/generate/activation-requests/'
            + selectedPlayer.value
            + '/'
            + `?is_approved=${approved}`

          isLoading.value = true

          axios
            .post(url1, data)
            .then(response => {
              isLoading.value = false
              isApproved.value = approved
              isDeleted.value = !approved

              getAccounts(url.value)
              
              if (data.expiration_date) {
                data.expiration_date = null
              }
            })
            .catch(err => {
              isLoading.value = false

              if (err.response.status == 400) {
                errors.value = err.response.data
                return
              }

              hasError.value = true
              
            })
          
          modalIsOpen.value = false
        }
      /**
       * End of Methods
       */

      const {pageNumber, limit, next, previous} = page(getAccounts)
      
      provide('selectedPlayer', selectedPlayer)
      provide('modalIsOpen', modalIsOpen)
      provide('activateAccount', activateAccount)
      provide('errors', errors)

      return {
        accounts,
        next,
        previous,
        selectedPlayer,
        modalIsOpen,
        isApproved,
        errors,
        isDeleted,
        activateAccount
      }
    }
  }
</script>