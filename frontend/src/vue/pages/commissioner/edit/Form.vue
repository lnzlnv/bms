<template>
  
  <div class="p-[1em] mb-[2rem]">
    <div>
      <button>General</button>
    </div>
    
    <form class="form-1 p-[1em]">
      <div class="xl:flex flex-row-reverse gap-[20px]">
        <PlayerImage />
        <div class="lg:grid lg-grid-2-column gap-[20px]">
          <PlayerInfo />
          <PlayerAttributes />
        </div>
      </div>
    </form>

    <div class="text-right mt-[3.438rem]">
        <button class="btn-7">Submit to Comm.</button>
      </div>
  </div>
</template>

<script>
  import TextInput from './TextInput.vue';
  import NumberInput from './NumberInput.vue';
  import PlayerInfo from './PlayerInfo.vue';
  import PlayerAttributes from './PlayerAttributes.vue';
  import PlayerImage from './PlayerImage.vue';

  export default {
    components: {
      TextInput,
      NumberInput,
      PlayerInfo,
      PlayerAttributes,
      PlayerImage
    }
  }
</script>