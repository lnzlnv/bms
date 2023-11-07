<template>
  <div class="mb-[1rem]">
    <h2 class="hero__title">Bucal Highlights</h2>
    <div 
      class="slider-1 relative mb-[1rem] min-h-[300px]" 
      id="js-slider"
    >
      <p
        v-if="highlights.length == 0"
        class="text-1 text-center"
      >
        No available highlights.
      </p>
      <div
        v-show="highlights.length > 1"
        class="slider-1__nav flex items-center justify-between">
        <button 
          @click="changeCurrent('minus')"
          class="h-[max-content] btn-slider left flex"
        >
          <img   
            class="img-14 rotate-1"
            :src="rightArrow" 
            alt=""
          >
        </button>

        <button 
          @click="changeCurrent('plus')"
          class="h-[max-content] btn-slider right flex"
        >
          <img
            class="img-14"
            :src="rightArrow" 
            alt=""
          >
        </button>
      </div>

      <div class="slider-1__container flex" id="js-slider-container">
        <div 
          v-for="highlight, index in highlights"
          :key="highlight.id"
          class="slider-1__content js-slider-content"
        >
          <video 
            class="hero__highlights js-video" 
            controls
            muted
            loop
            :autoplay="index == 1 || highlights.length == 1"
          >
            <source 
              :src="highlight.video" 
              :type="highlight.video_type"
            >
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
    </div>

    <div v-if="highlights.length > 1" class="flex justify-center gap-[5px]">
      <button
        v-for="highlight, index in highlights.length-2"
        :key="highlight.id"
        :class="current == index+1 ? 'active' : ''"
        class="btn-slider-nav"
        @click="current = index+1"
      >
      </button>
    </div>
  </div>
</template>
<script>
  import axios from 'axios';
  import { onBeforeMount, onMounted, onUpdated, ref, watch } from 'vue'; 
  import addAtStartAndEnd from '@composables/landing/addAtStartAndEnd.js'
  import slider1 from '@composables/slider-1';
  import rightArrow from '@images/right-arrow.png'

  export default {
    setup() {
      const highlights = ref([])
      const [
        current,
        setSlider, 
        translateContainer, 
      ] = slider1(highlights)
      const videos = ref([])

      onMounted(() => {
        
      })

      onBeforeMount(() => {
        const url = '/api/landing/highlights/public/'

        axios
          .get(url)
          .then(response => {
            if (response.data.length > 1) {
              highlights.value = addAtStartAndEnd(response.data)
            } else {
              highlights.value = response.data
            }
          })
      })

      watch(
        current,
        (newVal, oldVal) => {
          if(highlights.value.length == 1) {
            return
          }

          videos.value[newVal].play()
          videos.value[oldVal].pause()
          translateContainer()
        }
      )

      watch(
        highlights,
        () => {
          setTimeout(() => {
            videos.value = document.querySelectorAll('.js-video')
          }, 1000)

          if (highlights.value.length > 1) {
            setSlider()
          }
        }
      )

      const changeCurrent = (operation) => {
        switch (operation) {
          case 'plus':
            current.value += 1
            break;
          case 'minus':
            current.value -= 1
            break
          default:
            break;
        }
      }

      return {
        highlights,
        current,
        rightArrow,
        changeCurrent
      }
    }
  }
</script>