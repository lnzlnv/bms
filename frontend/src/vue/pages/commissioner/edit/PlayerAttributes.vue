<template>
  <div class="md:grid gap-[20px] md-grid-2-column-2">
    <div class="lg:grid lg-grid-2-row-1">
      <OffensiveAttributes />

      <MentalAttributes />
    </div>

    <div class="lg:grid lg-grid-2-row-2">
      <DefensiveAttributes />
    
      <PhysicalAttributes />
    </div>
  </div>
</template>

<script>
  import DefensiveAttributes from './DefensiveAttributes.vue';
  import MentalAttributes from './MentalAttributes.vue';
  import OffensiveAttributes from './OffensiveAttributes.vue';
  import PhysicalAttributes from './PhysicalAttributes.vue';

  export default {
    components: {
      OffensiveAttributes,
      MentalAttributes,
      DefensiveAttributes,
      PhysicalAttributes
    }
  }
</script>