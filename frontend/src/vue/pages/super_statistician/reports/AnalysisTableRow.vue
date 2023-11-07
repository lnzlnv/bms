<template>
  <tr>
    <td class="table-4__data">
      {{ col1 }}
    </td>
    <td class="table-4__data">
      {{ col2 }}
    </td>
    <td class="table-4__data">
      {{ col3 }}
    </td>
  </tr>
</template>

<script>
  export default {
    props: {
      col1: String | Number,
      col2: String | Number,
      col3: String | Number
    },
    setup(props){
      return {
        ...props
      }
    }
  }
</script>