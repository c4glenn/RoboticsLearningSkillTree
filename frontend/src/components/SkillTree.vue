<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { VueFlow, type Node, type Edge } from '@vue-flow/core';
import api from '@/api';

const nodes = ref<Node[]>([]);
const edges = ref<Edge[]>([]);

onMounted(async () => {
  try {
    const response = await api.get('tree/skill-tree/');
    nodes.value = response.data.nodes;
    edges.value = response.data.edges;
  } catch (error) {
    console.error('Error fetching skill tree data:', error);
  }
});

</script>


<template >
    <div class="h-screen w-full">

  <VueFlow
    v-model:nodes="nodes"
    v-model:edges="edges"
    :fit-view="true"
    class="h-full w-full bg-gray-900"
  />
      </div>

</template>

<style>
@import "@vue-flow/core/dist/style.css";
@import "@vue-flow/core/dist/theme-default.css";


</style>