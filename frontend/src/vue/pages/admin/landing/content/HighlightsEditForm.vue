<template lang="">
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
      @submit.prevent="editHighlight"
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

      <div>
        <input
          @change="setVideo"
          ref="video"
          class="input-field-3"
          type="file"
          name="highlights"
          id="highlights"
          accept="video/*"
          hidden="hidden"
        />

        <DragAreaVideo 
          :videoUrl="videoUrl"
          forInput="highlights"
          dragAreaName="js-drag-area"
          :videoType="videoType"
        />

        <Errors 
        :errors="errors.video"
      />
      </div>

      <div class="text-right">
        <button class="btn-7 mt-[1rem]">Edit Highlights</button>
      </div>                                        
    </form>
  </div>
</template>
<script>
  import { inject, onMounted, reactive, ref } from 'vue';
  import LoadingSpinner from '@templates/LoadingSpinner.vue';
  import Errors from '@pages/admin/schedules/create/Errors.vue';
  import closeIcon from '@images/close-icon.svg'
  import axios from 'axios';
  import fileDragAndDrop from '@composables/fileDragAndDrop.js'
  import DragAreaVideo from '@components/DragAreaVideo.vue';

  export default {
    components: {
      LoadingSpinner,
      Errors,
      DragAreaVideo
    },
    setup() {
      const errors = ref({})
      const isLoading = ref(false)
      const modalIsOpen = inject('modalIsOpen', modalIsOpen)
      const selectedHighlight = inject('selectedHighlight', selectedHighlight)
      const hasError = inject('hasError', hasError)
      const video = ref(null)
      const isEdited = inject('isEdited', isEdited)
      const data = reactive({
        video: null
      })
      const videoUrl = ref(null)
      const videoType = ref(null)

      onMounted(() => {
        fileDragAndDrop(
          'js-drag-area', 
          videoUrl, 
          data, 
          'video',
          'video',
          videoType
        )

        if (typeof selectedHighlight.value.image == 'object') {
          let container = new DataTransfer(); 
          container.items.add(selectedHighlight.value.image)
          video.value.files = container.files
          setVideo()
          return
        }
        isLoading.value = true
        axios
          .get(selectedHighlight.value.video, { responseType: 'blob' })
          .then(res => {
            const blob = res.data
            
            blob.lastModifiedDate = new Date();
            blob.name = selectedHighlight.value.video_name

            const file = new File(
              [blob], 
              selectedHighlight.value.video_name, 
              {
                type: blob.type
              }
            )

            let container = new DataTransfer(); 
            container.items.add(file)

            video.value.files = container.files
            setVideo()
            isLoading.value = false
          })
          .catch(err => {
            hasError.value = true
            isLoading.value = false
          })
      })

      const editHighlight = () => {
        isLoading.value = true
        const url = '/api/landing/highlights/'
          + selectedHighlight.value.id
          + '/'
        
        axios
          .put(
            url, 
            data,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then(response => {
            for (const key in response.data) {
              selectedHighlight.value[key] = response.data[key]
            }

            isLoading.value = false
            modalIsOpen.value = false
            isEdited.value = true
          })
          .catch(err => {
            hasError.value = true
          })
          
      }

      const setVideo = () => {
        data.video = video.value.files[0]

        if (data.video) {
          videoUrl.value = URL.createObjectURL(data.video)
          return
        }
        
        videoUrl.value = null
      }

      return {
        errors,
        isLoading,
        closeIcon,
        modalIsOpen,
        video,
        videoUrl,
        videoType,
        setVideo,
        editHighlight
      }
    }
  }
</script>