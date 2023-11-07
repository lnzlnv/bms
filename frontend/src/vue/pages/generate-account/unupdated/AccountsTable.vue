<template>
  <div>
    <table class="table-1">
      <thead>
        <tr>
          <th class="table-1__header text-left">Username</th>
          <th class="table-1__header text-left">Email</th>
          <th class="table-1__header text-left">User Role</th>
          <th class="table-1__header text-left"></th>
        </tr>
      </thead>
      <tbody v-if="accounts.results && Object.keys(accounts.results).length != 0">
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
                @click="sendEmail(account.id)"
                class="btn-9"
              >
                Email
              </button>
              <button
                class="btn-10"
                @click="deleteAccount(account.id)"
              >
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr class="table-1__row flex flex-col lg:table-row">
          <td 
            class="table-1__data empty lg:table-cell"
            colspan="4"
          >
            All accounts has been updated.
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
  import { computed, inject, onBeforeMount, ref } from 'vue';
  import  { page } from '@pages/admin/teams/all/composables.js'
  import normalizeData from '@composables/normalize-data.js'
  import axios from 'axios';

  export default {
    setup() {
      const accounts = ref({})
      const hasError = inject('hasError', hasError)
      const isLoading = inject('isLoading', isLoading)
      const emailSent = inject('emailSent', emailSent)

      onBeforeMount(() => {
        getAccounts(url.value)
      })

      /**
       * Computed
       */
        const url = computed(() => {
          return '/api/account/generate/'
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
              accounts.value = normalizeData(response.data)
              isLoading.value = false
            })
            .catch(err => {
              isLoading.value = false
              hasError.value = true
            })
        }

        const deleteAccount = (id) => {
          const delUrl = '/api/account/generate/delete/user-'
            + id
            + '/'

            isLoading.value = true

            axios
            .delete(delUrl)
            .then(response => {
              isDeleted.value = true
              getAccounts(url.value)
              isLoading.value = false
            })
            .catch(err => {
              hasError.value = true
              isLoading.value = false
            })
        }

        const sendEmail = (id) => {
          const url = '/api/account/generate/send-email/user-'
            + id
            + '/'

          isLoading.value = true
          
          axios
            .post(url)
            .then(response => {
              emailSent.value = true
              isLoading.value = false
            })
            .catch(err => {
              hasError.value = true
              isLoading.value = false
            })
        }
      /**
       * End of Methods
       */

      const {pageNumber, limit, next, previous} = page(getAccounts)

      return {
        deleteAccount,
        sendEmail,
        accounts,
        next,
        previous,
        url
      }
    }
  }
</script>