<template>
  <div class="text-center mb-[2.5rem]">
    <button class="btn-8 mb-[1rem]">
      Randomize Attributes
    </button>

    <div>
      <img 
        class="img-4"
        :src="profilePic" 
        alt="player profile pic" 
      />

      <button class="btn-8 mt-[1rem]">Change Pic</button>
    </div>
  </div>
</template>

<script>
  import profilePic from '@images/profile-pic.jpeg';

  export default {
    name: 'PlayerImage',
    setup() {
      return {
        profilePic
      }
    }
  }
</script>