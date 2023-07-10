<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  id: number;
  title?: string;
}>();

const link = computed(() => `https://www.v2ex.com/t/${props.id}`);
</script>

<template>
  <a :href="link">{{ title || link }} </a>
</template>
