<template>
  <label 
    :class="videoUrl ? 
      `uploaded drag-area flex justify-center items-center ${dragAreaName}`
      : `drag-area flex justify-center items-center ${dragAreaName}`"
    :for="forInput"
  >
    <div v-if="videoUrl">
      <video
          class="mb-[1rem] mx-auto max-h-[300px] object-cover"
          controls
        >
        <source 
          :src="videoUrl" 
          :type="videoType"
        >
        Your browser does not support the video tag.
      </video>
    </div>
    <div v-else>
      <img
        class="img-16 mx-auto"
        :src="videoIcon"
        alt="image icon"
      >
      <div 
        class="drag-area__text text-1 font-bold js-drag-text"
      >
        Drag & Drop to upload
      </div>
      <span class="link-4">
        or browse
      </span>
    </div>
  </label>
</template>

<script>
  import videoIcon from '@images/video-icon.png'
  
  export default {
    props: {
      videoUrl: String || null,
      forInput: String,
      dragAreaName: String,
      videoType: String || null
    },
    setup(props) {
      return {
        ...props,
        videoIcon
      }
    }
  }
</script>