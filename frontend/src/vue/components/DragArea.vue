<template>
  <label 
    :class="imageUrl ? 
      `uploaded drag-area flex justify-center items-center ${dragAreaName}`
      : `drag-area flex justify-center items-center ${dragAreaName}`"
    :for="forInput"
  >
    <div v-if="imageUrl">
      <img  
        class="mx-auto max-h-[300px] object-contain"
        :src="imageUrl" 
        alt=""
      >
    </div>
    <div v-else>
      <img
        class="img-16 mx-auto"
        :src="imageIcon"
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
  import imageIcon from '@images/image-icon.png'
  
  export default {
    props: {
      imageUrl: String || null,
      forInput: String,
      dragAreaName: String
    },
    setup(props) {
      return {
        ...props,
        imageIcon
      }
    }
  }
</script>