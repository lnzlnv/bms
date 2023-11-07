<template>
  <div>
    <label 
      class="label-1"
      :for="name"
    >
      {{ label }}
    </label>
    <input 
      class="input-field-3"
      type="date" 
      :name="name" 
      :id="name" 
    />
  </div>
</template>

<script>
  export default {
    name: 'DateInput',
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