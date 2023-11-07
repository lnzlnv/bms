<template>
  <div>
    <label 
      class="label-1"
      :for="name"
    >
      {{ label }}: 
    </label>
    <input 
      class="input-field-4"
      type="number" 
      :name="name" 
      :id="name"
      :value="value"
    />
  </div>
</template>

<script>
  export default {
    name: 'NumberInput',
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