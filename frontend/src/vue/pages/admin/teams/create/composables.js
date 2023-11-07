import { ref, watch } from 'vue'


const error = () => {
  const hasError = ref(false)

  watch(
    hasError,
    (isError) => {
      if (isError) {
        setTimeout(() => {
          hasError.value = false
        }, 5000)
      }
    }
  )

  return hasError
}


export { error }