<template>
  <div class="md:grid grid-2-column-2 mb-[2rem]">
    <div 
      v-if="game.is_approved_by_super_statistician"
      class="text-center title-2"
    > 
      <p>Approved by Lead Statistician:</p>
      <p>
        {{ game.approved_by_super_statistician.first_name }}
        {{ game.approved_by_super_statistician.last_name }}
      </p>
    </div>

    <div class="text-center">
      <button
        v-if="!game.is_approved_by_admin"
        @click="approvedReport"
        class="btn-22"
      >
        Approve Report
      </button>

      <div 
        v-if="game.is_approved_by_admin"
        class="title-2"
      >
        <p>Approved by:</p>
        <p>
          {{ game.approved_by_admin.first_name }}
          {{ game.approved_by_admin.last_name }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import host from '@composables/host.js';
import { inject, onMounted, ref } from 'vue';
  
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  
  export default {
    props: {
      game: {}
    },
    setup(props) {
      const gameId = ref(null)

      onMounted(() => {
        gameId.value = document.getElementById('js-game-id').value
      })

      const isApproved = inject('isApproved', isApproved)

      const game = inject('game', game)

      const approvedReport = () => {
        const url = '/api/games-for-admin-approval/' + gameId.value + '/'
        axios
          .post(url)
          .then(response => {
            isApproved.value = true
            game.value.is_approved_by_admin = true
          })
          .catch(err => {
            console.log(err)
          })
      }

      return {
        ...props,
        approvedReport
      }
    }
  }
</script>