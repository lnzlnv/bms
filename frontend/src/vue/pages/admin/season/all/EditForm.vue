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
        @click="modalIsOpen = false"
      >
        <img 
        class="icon-2"
        :src="closeIcon" 
        alt="close icon"
      />
      </button>
    </div>

    <form 
      @submit.prevent="editSeason"
    >
      <Errors 
        :errors="errors.non_field_errors"
      />

      <div class="mb-[1rem]">
        <input
          v-model="season.year"
          class="input-field-3"
          type="number"
          placeholder="Season Number"
          required="required"
        />
        
        <Errors 
          :errors="errors.year"
        />
      </div>

      <div>
        <input 
          @change="addImage"
          class="input-field-3"
          type="file" 
          accept="image/*"
          ref="image"
          id="logo"
          hidden="hidden"
        >

        <DragArea 
          :imageUrl="imageUrl"
          forInput="logo"
          dragAreaName="js-drag-area"
        />

        <Errors 
          :errors="errors.logo"
        />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Edit Season</button>
      </div>
    </form>
  </div>
</template>

<script>
  import axios from 'axios';

  import host from '@composables/host.js';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import closeIcon from '@images/close-icon.svg'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import { onMounted, reactive, ref, watch, inject, season } from 'vue';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';

  export default {
    props: {
      selectedSeason: {},
      editSuccess: Function
    },
    components: {
      Errors,
      LoadingSpinner,
      DragArea
    },
    setup(props) {
      const image = ref({})
      const isLoading = ref(false)
      const season = reactive({})
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop(
          'js-drag-area',
          imageUrl,
          season,
          'logo'
        )
        for (const key in props.selectedSeason) {
          season[key] = props.selectedSeason[key]
        }

        if (typeof props.selectedSeason.logo == 'object') {
          let container = new DataTransfer(); 
          container.items.add(props.selectedSeason.logo)
          image.value.files = container.files
          addImage()
          return
        }
        isLoading.value = true
        axios
          .get(props.selectedSeason.logo, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = props.selectedSeason.logo_name

            const file = new File(
              [blob], 
              props.selectedSeason.logo_name, 
              {
                type: blob.type
              }
            )

            let container = new DataTransfer(); 
            container.items.add(file)

            image.value.files = container.files
            addImage()
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      const errors = ref({})

      const editSeason = () => {
        isLoading.value = true
        const url = host + '/api/seasons/' + props.selectedSeason.id + '/'
        
        axios
          .put(
            url, 
            season,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            props.editSuccess()
            for (const key in season) {
              props.selectedSeason[key] = season[key]
            }
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            if (err.request == undefined || err.request.status != 400) {
              hasError.value = true
              return
            }

            errors.value = err.response.data
          })
      }

      const addImage = () => {
        season.logo = image.value.files[0]

        if (season.logo) {
          imageUrl.value = URL.createObjectURL(season.logo)
          return
        }
        
        imageUrl.value = null
      }

      const hasError = inject('hasError', hasError)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)

      return {
        errors,
        ...props,
        image,
        season,
        modalIsOpen,
        closeIcon,
        isLoading,
        imageUrl,
        editSeason,
        addImage,
      }
    }
  }
</script>

<style lang="scss" scoped>

</style>