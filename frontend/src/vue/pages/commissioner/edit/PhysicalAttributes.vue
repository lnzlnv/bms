<template>
  <div>
    <h4 class="label-1">Physical Attributes</h4>

    <div class="lg:flex flex-col justify-evenly input-group calc-h">
      <NumberInput 
        name="height"
        label="Height"
        value="3"
      />

      <NumberInput 
        name="jump"
        label="Jump"
        value="23"
      />

      <NumberInput 
        name="quickness"
        label="Quickness"
        value="23"
      />

      <NumberInput 
        name="speed"
        label="Speed"
        value="23"
      />

      <NumberInput 
        name="power"
        label="Power"
        value="23"
      />

      <NumberInput 
        name="stamina"
        label="Stamina"
        value="23"
      />

      <TextInput 
        name="injury_risk"
        label="Injury Risk"
        value="Medium"
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
