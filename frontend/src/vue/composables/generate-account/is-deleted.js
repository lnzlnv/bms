import { ref, watch } from "vue";

const deleted = () => {
  const isDeleted = ref(false)

  watch(
    isDeleted,
    (hasDeleted) => {
      if (hasDeleted) {
        setTimeout(() =>{
          isDeleted.value = false
        }, 5000)
      }
    }
  )

  return { isDeleted }
}

export default deleted