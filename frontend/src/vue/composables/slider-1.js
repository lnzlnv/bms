import { computed, ref, watch } from 'vue'

export default (storage) => {
  if (!storage) { return }

  const current = ref(1)
  let container = null
  const numOfElements = computed(() => {
    return storage.value.length
  })

  const setSlider = () => {
    const slider = document.getElementById('js-slider')
  
    if (slider == null) { return }

    container = document.getElementById('js-slider-container')
    translateContainer()

    container.addEventListener('transitionend', () => {
      if (current.value == numOfElements.value-1) {
        container.style.transition = 'none'
        current.value = 1
        translateContainer()
      } else if (current.value == 0) {
        container.style.transition = 'none'
        current.value = numOfElements.value - 2
        translateContainer()
      } else {
        // do nothing
      }
      setTimeout(() => {
        container.style.transition = 'all ease-in-out 250ms'
      })
    })

    setTimeout(() => {
      container.style.transition = 'all ease-in-out 250ms'
    }, 1000)
  } 

  const translateContainer = () => {
    const translate = `translate(-${container.clientWidth * current.value}px)`
    container.style.transform = translate
  }

  return [
    current,
    setSlider,
    translateContainer,
  ]
}