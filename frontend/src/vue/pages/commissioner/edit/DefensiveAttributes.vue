<template>
  <div class="mb-[2.5rem]">
    <h4 class="label-1">Defensive Attributes</h4>

    <div class="lg:flex flex-col justify-evenly input-group calc-h">
      <NumberInput
        name="marking"
        label="Marking"
        value="1"
      />
      <NumberInput
        name="stealing"
        label="Stealing"
        value="1"
      />
      <NumberInput
        name="blocking"
        label="Blocking"
        value="1"
      />
      <NumberInput
        name="rebound_def"
        label="Rebound Def"
        value="1"
      />
    </div>
  </div>
</template>

<script>
  import TextInput from './TextInput.vue';
  import NumberInput from './NumberInput.vue';
  
  export default {
    name: 'DefensiveAttributes',
    components: {
      TextInput,
      NumberInput
    }
  }
</script>