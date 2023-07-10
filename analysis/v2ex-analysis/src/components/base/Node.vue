<script setup lang="ts">

const props = defineProps<{
  node: string;
}>();

</script>

<template>
  <a :href="`https://www.v2ex.com/go/${node}`">{{ node }} </a>
</template>
