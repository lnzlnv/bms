<template>
  <div>
    <div class="max-w-[800px] px-[1em] mx-auto">
      <h1 class="schedule__title bg-skew-2 w-max mb-[2rem]">
        Update Profile
      </h1>
      
      <form @submit.prevent="updateProfile" class="form-1 p-[1em] relative">
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
            v-model="userData.username"
            class="input-field-3"
            type="text" 
            name="username" 
            id="username"
            placeholder="Username"
            title="Username"
            required="required"
          >
          <Errors 
            :errors="errors.username"
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
            title="Email address"
            required="required"
          >
          <Errors 
            :errors="errors.email"
          />
        </div>

        <div class="mb-[1rem]">
          <input 
            v-model="userData.first_name"
            class="input-field-3"
            type="text" 
            name="first_name" 
            id="first_name"
            placeholder="First Name"
            title="First Name"
            required="required"
          >
          <Errors 
            :errors="errors.first_name"
          />
        </div>

        <div class="mb-[1rem]">
          <input 
            v-model="userData.last_name"
            class="input-field-3"
            type="text" 
            name="last_name" 
            id="last_name"
            placeholder="Last Name"
            title="Last Name"
            required="required"
          >
          <Errors 
            :errors="errors.last_name"
          />
        </div>

        <div class="mb-[1rem]">
          <input 
            v-model="userData.password1"
            class="input-field-3"
            type="password" 
            name="password1" 
            id="password1"
            placeholder="Password"
            title="Password"
            required="required"
          >
          <Errors 
            :errors="errors.password1"
          />
        </div>

        <div>
          <input 
            v-model="userData.password2"
            class="input-field-3"
            type="password" 
            name="password2" 
            id="password2"
            placeholder="Retype password"
            title="Retype password"
            required="required"
          >
          <Errors 
            :errors="errors.password2"
          />
        </div>
        
        <div class="text-right">
          <button class="btn-7 mt-[1rem]">
            Update Profile
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import { onBeforeMount, reactive, ref } from 'vue';
  import axios from 'axios';
  import setCsrfToken from '@composables/csrf-token.js';

  setCsrfToken()

  export default {
    components: {
      LoadingSpinner,
      Errors
    },
    setup() {
      const errors = ref({})
      const isLoading = ref(false)
      const userData = reactive({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password1: '',
        password2: ''
      })
      let userID = 0

      onBeforeMount(() => {
        userID = document.getElementById('js-user-id').value
      })


      /**
       * Methods
       */
        const updateProfile = () => {
          const passwordsAreTheSame = userData.password1 == userData.password2
          if (!passwordsAreTheSame) {
            errors.value['password2'] = ['Passwords does not match.']
            return
          }
          const url = '/api/user/profile/update/user-'
            + userID
            + '/'

          isLoading.value = true

          axios
            .post(url, userData)
            .then(response => {
              isLoading.value = false
              window.location.replace('/sign-in/')
              errors.value = null
            })
            .catch(err => {
              errors.value = err.response.data
              isLoading.value = false
            })
        }
      /**
       * End of Methods
       */

      return {
        errors,
        isLoading,
        userData,
        updateProfile
      }
    }
  }
</script>