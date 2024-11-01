<template>
  <div class="flex flex-col items-center justify-center p-4 min-h-screen transition-all duration-300">
    <div class="w-full max-w-3xl">
      <h2 class="text-4xl font-semibold text-darkBlue mb-10 text-center">Благотворительные Организации</h2>
      <div v-if="organizations.length" class="space-y-6">
        <Post 
          v-for="org in organizations" 
          :key="org.id" 
          :post="org" 
        />
      </div>
      <div v-else class="text-center text-gray-500">
        Нет доступных организаций для поддержки.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue';
import Post from './Post.vue';

const organizations = ref([]);

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/charity_organizations');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    organizations.value = data; 
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
  }
});

provide('organizations', organizations);
</script>

<style scoped>
</style>
