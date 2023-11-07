<template>
  <div class="mb-[2.5rem] h-full">
    <h2 class="label-1">Player Information</h2>

    <div class="lg:flex flex-col justify-between input-group calc-h">
      <TextInput
        name="id"
        label="ID"
        value="123"
      />
      <TextInput
        name="identity"
        label="Identity"
        value="Identity"
      />
      <TextInput
        name="last_name"
        label="Last Name"
        value="Lasst Name"
      />
      <TextInput
        name="first_name"
        label="First Name"
        value="First Name"
      />
    
      <TextInput
        name="nationality"
        label="Nationality"
        value="Philippines"
      />
      <TextInput
        name="citizenship"
        label="Citizenship"
        value="Filipino"
      />
      <TextInput
        name="school"
        label="School"
        value="ADNU"
      />
      <TextInput
        name="team"
        label="Team"
        value="ADNU"
      />
      <TextInput
        name="team"
        label="Team"
        value="ADNU"
      />
      <TextInput
        name="position"
        label="Position"
        value="Center"
      />
    
      <div>
        <DateInput
          name="birthdate"
          label="Date of Birth"
        />
        <NumberInput
          name="age"
          label="Age"
          value="24"
        />
      </div>
      <div>
        <NumberInput
          name="contract"
          label="Contract (years)"
          value="3"
        />
        <NumberInput
          name="potential"
          label="Potential"
          value="3"
        />
      </div>
    </div>
  </div>
</template>

<script>
  import TextInput from './TextInput.vue';
  import NumberInput from './NumberInput.vue';
  import DateInput from './DateInput.vue';
  
  export default {
    name: 'PlayerInfo',
    components: {
      TextInput,
      NumberInput,
      DateInput
    }
  }
</script>