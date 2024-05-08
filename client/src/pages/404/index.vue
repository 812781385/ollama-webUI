<script lang="ts" setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

onMounted(() => {
  const route = useRoute()
  console.log(route.params)
})
</script>

<template>
  <div>
    <h1>404 not find</h1>
  </div>
</template>
