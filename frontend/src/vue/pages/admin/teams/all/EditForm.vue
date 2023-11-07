<template>
  <div class="container-7 relative">
    <div 
      v-if="isLoading"
      class="loading-2 flex justify-center items-center"
    >
      <LoadingSpinner />
    </div>

    <div class="text-right mb-[1rem]">
      <button
        @click="closeModal"
      >
        <img 
        class="icon-2"
        :src="closeIcon" 
        alt="close icon"
      />
      </button>
    </div>

    <form @submit.prevent="editTeam">
      <div class="non-field-errors mb-[1rem]">
          <Errors 
            :errors="errors.non_field_errors"
          />
        </div>

        <div class="mb-[1rem]">
          <select
            v-model="team.season"
            class="input-field-3"
            required="required"
          >
          <option value="" disabled selected>Select Season</option>
          <option
            v-for="season in options.seasons"
            :key="season.id"
            :value="season.id"
          >
            {{ season.year }}
          </option>
          </select>

          <Errors 
            :errors="errors.division"
          />
        </div>

        <div class="mb-[1rem]">
          <select
            v-model="team.division"
            class="input-field-3"
            required="required"
          >
          <option value="" disabled selected>Select Division</option>
          <option
            v-for="division in options.divisions"
            :key="division[0]"
            :value="division[0]"
          >
            {{ division[1] }}
          </option>
          </select>

          <Errors 
            :errors="errors.division"
          />
        </div>

        <div class="mb-[1rem]">
          <input
            v-model="team.name"
            class="input-field-3"
            type="text"
            name="name"
            id="name"
            placeholder="Name"
            required="required"
          />

          <Errors 
            :errors="errors.name"
          />
        </div>

        <div>
          <input 
            @change="addLogo"
            class="input-field-3"
            id="logo"
            type="file"
            accept=".png"
            ref="logo"
            hidden="hidden"
          >

          <DragArea 
            :imageUrl="logoUrl"
            forInput="logo"
            dragAreaName="js-drag-area"
          />

          <Errors 
            :errors="errors.logo"
          />
        </div>

        <div class="text-right">
          <button class="btn-7 mt-[1rem]">Edit Team</button>
        </div>
    </form>
  </div>
</template>

<script>
  import { onMounted, ref, inject, reactive } from 'vue';
  import axios from 'axios';
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import host from '@composables/host.js';
  import closeIcon from '@images/close-icon.svg'
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';

  export default {
    name: 'EditForm',
    props: {
      options: {},
      selectedTeam: {},
      isEdited: Function
    },
    components: {
      Errors,
      LoadingSpinner,
      DragArea
    },
    setup(props) {
      const errors = ref({})
      const logo = ref(null)
      const team = reactive({})
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const hasError = inject('hasError', hasError)
      const isLoading = ref(false)
      const logoUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop('js-drag-area', logoUrl, team, 'logo')

        for (const key in props.selectedTeam) {
          team[key] = props.selectedTeam[key]
        }
        team['season'] = props.options.seasons[0].id

        if (typeof props.selectedTeam.logo == 'object') {
          let container = new DataTransfer(); 
          container.items.add(props.selectedTeam.logo)
          logo.value.files = container.files
          addLogo()
          return
        }

        
        isLoading.value = true
        axios
          .get(props.selectedTeam.logo, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = props.selectedTeam.logo_name

            const file = new File(
              [blob], 
              props.selectedTeam.logo_name, 
              {
                type: blob.type
              }
            )

            let container = new DataTransfer(); 
            container.items.add(file)

            logo.value.files = container.files
            addLogo()
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      const addLogo = () => {
        team.logo = logo.value.files[0]

        if (team.logo) {
          logoUrl.value = URL.createObjectURL(team.logo)
          return
        } 
          
        logoUrl.value = null
      }

      const editTeam = () =>  {
        isLoading.value = true
        const url = host + '/api/teams/' + props.selectedTeam.id + '/'

        axios
          .put(
            url, 
            team,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            for (const key in team) {
              props.selectedTeam[key] = team[key]
            }

            props.isEdited()
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            if (err.request.status == 400) {
              errors.value = err.response.data
              return
            }

            hasError.value = true
          })
      }

      const closeModal = () => {
        modalIsOpen.value = false
      }

      return {
        errors,
        ...props,
        logo,
        closeIcon,
        team,
        isLoading,
        logoUrl,
        editTeam,
        closeModal,
        addLogo,
      }
    }
  }
</script>