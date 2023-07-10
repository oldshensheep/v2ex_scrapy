<script setup lang="ts">

const props = defineProps<{
  username: string;
}>();
</script>

<template>
  <a :href="`https://www.v2ex.com/member/${username}`">{{ username }} </a>
</template>
