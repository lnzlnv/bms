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

    <form 
      @submit.prevent="editAnnouncement" 
      class="relative"
    >
      <div 
        v-if="isLoading"
        class="loading-2 flex justify-center items-center"
      >
        <LoadingSpinner />
      </div>

      <Errors
        :errors="errors.non_field_errors"
      />

      <div class="mb-[1rem]">
        <input
          v-model="announcement.date_format_1"
          class="input-field-3"
          type="datetime-local"
          placeholder="Publish Date"
        />

        <Errors
          :errors="errors.publish_date"
        />
      </div>

      <div>
        <input 
          @change="getImage"
          class="input-field-3"
          type="file"
          accept="image/*"
          ref="image"
          id="image"
          hidden="hidden"
        >

        <DragArea 
          :imageUrl="imageUrl"
          forInput="image"
          dragAreaName="js-drag-area"
        />

        <Errors
          :errors="errors.image"
        />
      </div>

      <div class="text-right">
          <button class="btn-7 mt-[1rem]">Edit Announcement</button>
        </div>
    </form>
  </div>
</template>

<script>
  import { onMounted, ref, inject, reactive  } from 'vue';
  import axios from 'axios';
  import host from '@composables/host.js';
  import closeIcon from '@images/close-icon.svg'
  import LoadingSpinner from '@templates/LoadingSpinner.vue'
  import Errors from '@pages/admin/schedules/create/Errors.vue'; 
  import DragArea from '@components/DragArea.vue';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'

  export default {
    props: {
      selectedAnnouncement: {},
      editSuccess: Function
    },
    components: {
    Errors,
    LoadingSpinner,
    DragArea,
    DragArea
},
    setup(props) {
      const image = ref(null)
      const errors = ref({})
      const isLoading = ref(false)
      const announcement = reactive({})
      const hasError = inject('hasError', hasError)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const imageUrl = ref(null)

      onMounted(() => {
        fileDragAndDrop(
          'js-drag-area',
          imageUrl,
          announcement,
          'image'
        )

        for (const key in props.selectedAnnouncement) {
          announcement[key] = props.selectedAnnouncement[key]
        }

        if (typeof props.selectedAnnouncement.image == 'object') {
          let container = new DataTransfer(); 
          container.items.add(props.selectedAnnouncement.image)
          image.value.files = container.files
          getImage()
          return
        }

        isLoading.value = true
        axios
          .get(props.selectedAnnouncement.image, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = props.selectedAnnouncement.image_name

            const file = new File(
              [blob], 
              props.selectedAnnouncement.image_name, 
              {
                type: blob.type
              }
            )

            let container = new DataTransfer(); 
            container.items.add(file)

            image.value.files = container.files
            getImage()
            isLoading.value = false
          })
          .catch(err => {
            isLoading.value = false
            hasError.value = true
          })
      })

      const editAnnouncement = () => {
        isLoading.value = true
        const url = host + '/api/announcements/' 
          + props.selectedAnnouncement.id + '/'
        
        announcement.publish_date = announcement.date_format_1
        axios
          .put(
            url, 
            announcement,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            for(const key in response.data) {
              props.selectedAnnouncement[key] = response.data[key]
            }

            props.editSuccess()
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

      const getImage = () => {
        announcement.image = image.value.files[0]
        
        if (announcement.image) {
          imageUrl.value = URL.createObjectURL(announcement.image)
          return
        }
        
        imageUrl.value = null
      }

      return {
        image,
        ...props,
        errors,
        announcement,
        modalIsOpen,
        closeIcon,
        isLoading,
        imageUrl,
        editAnnouncement,
        getImage,
      }
    }
  }
</script>