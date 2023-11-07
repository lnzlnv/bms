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
      @submit.prevent="editBanner"
    >
      <div class="non-field-errors mb-[1rem]">
        <Errors
          :errors="errors.non_field_errors"
        />
      </div>

      <div class="mb-[1rem]">
        <select
          v-model="banner.season"
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
          :errors="errors.season"
        />
      </div>

      <div class="mb-[1rem]">
        <select
          v-model="banner.division"
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
          v-model="banner.date_format_2"
          class="input-field-3"
          type="datetime-local"
          required="required"
          title="Expiration Date"
        >

        <Errors
          :errors="errors.date"
        />
      </div>

      <div>
        <input 
          @change="addImage"
          class="input-field-3"
          type="file"
          accept=".png"
          ref="image"
          id="image"
          hidden="hidden"
        >

        <DragArea 
          forInput="image"
          dragAreaName="js-drag-area"
          :imageUrl="imageUrl"
        />

        <Errors
          :errors="errors.image"
        />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Edit Banner</button>
      </div>
    </form>
  </div>
</template>

<script>
  import axios from 'axios';
  import { onMounted, ref, inject, reactive } from 'vue';
  import Errors from '@pages/admin/schedules/create/Errors.vue'; 
  import host from '@composables/host.js';
  import closeIcon from '@images/close-icon.svg'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragArea from '@components/DragArea.vue';

  export default {
    props: {
      options: {},
      selectedBanner: {},
      closeModal: Function,
      updateEditedBanner: Function,
      banners: {},
      season: Number,
      division: String,
      editSuccess: Function
    },
    components: {
      Errors,
      LoadingSpinner,
      DragArea
    },
    setup(props) {
      const image = ref(null)
      const errors = ref({})
      const hasError = inject('hasError', hasError)
      const banner = reactive({})
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const isLoading = ref(false)
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop('js-drag-area', imageUrl, banner, 'image')

        for (const key in props.selectedBanner) {
          banner[key] = props.selectedBanner[key]
        }

        if (typeof props.selectedBanner.image == 'object') {
          let container = new DataTransfer(); 
          container.items.add(props.selectedBanner.image)
          image.value.files = container.files
          addImage()
          return
        }

        isLoading.value = true
        axios
          .get(props.selectedBanner.image, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = props.selectedBanner.image_name

            const file = new File(
              [blob], 
              props.selectedBanner.image_name, 
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

      const editBanner = () => {
        isLoading.value = true
        banner.date = banner.date_format_2
        const url = host + '/api/game-schedule/banner/' 
          + props.selectedBanner.id + '/'
        
        axios
          .put(
            url, 
            banner,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            const bannerId = props.selectedBanner.id
            const data = response.data

            const seasonIsChanged = data.season != props.season
            const divisionIsChanged = data.division != props.division

            if ( seasonIsChanged || divisionIsChanged) {
              for(let i = 0; i < props.banners.results.length; ++i) {
                if(props.banners.results[i].id != data.id) {
                  continue
                }

                props.banners.results.splice(i, 1)
              } 
              return
            }

            for(let i = 0; i < props.banners.results.length; ++i) {
              if (props.banners.results[i].id == bannerId) {
                for (const key in data) {
                  props.banners.results[i][key] = data[key]
                }
              }
            }

            errors.value = {}
            modalIsOpen.value = false
            isLoading.value = false
            props.editSuccess()
          })
          .catch(err => {
            isLoading.value = false
            if (err.request == undefined || err.request.status != 400) {
              console.log(err)
              hasError.value = true
              return
            }

            errors.value = err.response.data
          })
      }

      const addImage = () => {
        banner.image = image.value.files[0]

        if (banner.image) {
          imageUrl.value = URL.createObjectURL(banner.image)
          return
        }
        
        imageUrl.value = null
      }

      return {
        ...props,
        image,
        errors,
        modalIsOpen,
        closeIcon,
        banner,
        isLoading,
        imageUrl,
        editBanner,
        addImage,
      }
    }
  }
</script>