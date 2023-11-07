<template>
  <div class="relative">
    <div 
      v-if="hasError"
      class="container-6 flex justify-center"
    >
      <div class="delete-1">
        An error occured!
      </div>
    </div>

    <div 
      v-if="isCreated"
      class="container-6 flex justify-center"
    >
      <div class="success-1">
        Generation of user is successful!
      </div>
    </div>

    <div class="max-w-[800px] px-[1em] mx-auto">
      <form @submit.prevent="generateAccount" class="form-1 p-[1em] relative">
        <div 
          v-if="isLoading"
          class="loading-2 flex justify-center items-center"
        >
          <LoadingSpinner />
        </div>
        
        <div class="non-field-errors mb-[1rem]">
          <Errors 
            :errors="errors.non_field_errors"
          />
        </div>

        <div class="mb-[1rem]">
          <input 
            v-model="userData.email"
            class="input-field-3"
            type="email" 
            name="email" 
            id="email" 
            placeholder="Email"
            title="Email"
            required="required"
          />
          <Errors 
            :errors="errors.email"
          />
        </div>

        <div class="mb-[1rem]">
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

        <div>
          <select 
            v-model="userData.user_role"
            class="input-field-3"
            name="user_role" 
            id="user_role"
            title="User Role"
            required="required"
          >
            <option value="" disabled selected>Select User Role</option>
            <option 
              v-for="role in options"
              :key="role[0]"
              :value="role[0]"
            >
              {{ role[1] }}
            </option>
          </select>

          <Errors 
            :errors="errors.user_role"
          />
        </div>

        <div class="text-right">
          <button class="btn-7 mt-[1rem]">
            Generate Account
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import setCsrfToken from '@composables/csrf-token.js';
  import { onBeforeMount, reactive, ref, watch } from 'vue';
  import axios from 'axios';
  import { error } from '@pages/admin/teams/create/composables.js'
  import LoadingSpinner from '@templates/LoadingSpinner.vue';


  setCsrfToken()
  export default {
    components: {
      Errors,
      LoadingSpinner
    },
    setup() {
      const errors = ref({})
      const hasError = error()
      const options = ref(null)
      const userData = reactive({
        email: null,
        expiration_date: null,
        user_role: ''
      })
      const isCreated = ref(false)
      const isLoading = ref(false)

      onBeforeMount(() => {
        const url = '/api/account/generate/options/'

        isLoading.value = true

        axios
          .get(url)
          .then(response => {
            options.value = response.data
            isLoading.value = false
          })
          .catch(err => {
            hasError.value = true
            isLoading.value = false
          })
      })

      /**
       * Methods
       */
        const generateAccount = () => {
          const url = '/api/account/generate/'

          isLoading.value = true
          axios
            .post(url, userData)
            .then(response => {
              isCreated.value = true
              userData.email = null
              userData.expiration_date = null
              userData.user_role = ''
              isLoading.value = false
              errors.value = {}
            })
            .catch(err => {
              isLoading.value = false
              if (err.response.status != 400) {
                hasError.value = true
                return
              }
              errors.value = err.response.data
            })
        }
      /**
       * End of Methods
       */

      /**
       * Watch
       */
        watch(
          isCreated,
          (created) => {
            if (created) {
              setTimeout(() => {
                isCreated.value = false
              }, 5000)
            }
          }
        )
      /**
       * End of Watch
       */

      return {
        errors,
        hasError,
        options,
        userData,
        isCreated,
        isLoading,
        generateAccount
      }
    }
  }
</script>