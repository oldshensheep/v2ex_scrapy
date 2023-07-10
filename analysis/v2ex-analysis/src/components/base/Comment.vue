<script setup lang="ts">
import { computed, toRefs } from 'vue';

const props = defineProps<{
  id: number;
  topicId: number;
  no: number;
  content?: string;
}>();

const link = computed(() => `https://www.v2ex.com/t/${props.topicId}?p=${Math.ceil(props.no / 100)}#r_${props.id}`);
</script>

<template>
  <a :href="link">
    <div v-if="!content">{{ link }}</div>
    <div v-else v-html="content"></div>
  </a>
</template>
