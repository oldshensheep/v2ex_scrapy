<script setup lang="ts">
const props = defineProps<{
  tag: string;
}>();

</script>

<template>
  <a :href="`https://www.v2ex.com/tag/${tag}`">{{ tag }} </a>
</template>
