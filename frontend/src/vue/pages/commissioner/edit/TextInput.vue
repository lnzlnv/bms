<template>
  <div class="mb-[1rem]">
    <label
      class="label-1" 
      :for="name"
    >
      {{ label }}: 
    </label>
    <input 
      class="input-field-3"
      type="text" 
      :name="name" 
      :id="name" 
      :value="value" 
    />
  </div>
</template>

<script>
  export default {
    name: 'TextInput',
    props: [
      'name',
      'label',
      'value'
    ],
    setup(props) {
      return {
        ...props
      }
    }
  }
</script>