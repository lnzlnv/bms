<template>
  <div class="mb-[2.5rem]">
    <h4 class="label-1">Offensive Attributes</h4>

    <div class="lg:flex flex-col justify-evenly input-group calc-h">
      <NumberInput
        name="three_pt_shooting"
        label="3P Shooting"
        value="3"
      />
      <NumberInput
        name="two_pt_shooting"
        label="2P Shooting"
        value="3"
      />
      <NumberInput
        name="two_pt_inside"
        label="2P Inside"
        value="3"
      />
      <NumberInput
        name="free_throws"
        label="Free Throws"
        value="3"
      />
      <NumberInput
        name="drive_scoring"
        label="Drive Scoring"
        value="3"
      />
      <NumberInput
        name="ball_handling"
        label="Ball Handling"
        value="3"
      />
      <NumberInput
        name="passing"
        label="Passing"
        value="3"
      />
      <NumberInput
        name="rebound_off"
        label="Rebound Off"
        value="3"
      />
    </div>
  </div>
</template>

<script>
  import TextInput from './TextInput.vue';
  import NumberInput from './NumberInput.vue';
  
  export default {
    name: 'OffensiveAttributes',
    components: {
      TextInput,
      NumberInput
    }
  }
</script>