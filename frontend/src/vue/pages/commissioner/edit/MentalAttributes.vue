<template>
  <div class="mb-[2.5rem] md:mb-0">
    <h4 class="label-1">Mental Attributes</h4>

    <div class="lg:flex flex-col justify-evenly input-group calc-h">
      <NumberInput
        name="experience"
        label="Experience"
        value="10"
      />
      <TextInput
        name="temperament"
        label="Temperament"
        value="Normal"
      />
      <TextInput
        name="clutch"
        label="Clutch"
        value="Yes"
      />
    </div>
  </div>
</template>

<script>
  import TextInput from './TextInput.vue';
  import NumberInput from './NumberInput.vue';
  
  export default {
    name: 'PhysicalAttributes',
    components: {
      TextInput,
      NumberInput
    }
  }
</script>