import { ref, watch } from "vue";

const success = () => {
  const isSuccess = ref(false)

  watch(
    isSuccess,
    (successful) => {
      if (successful) {
        setTimeout(() =>{
          isSuccess.value = false
        }, 5000)
      }
    }
  )

  return isSuccess
}

export default success