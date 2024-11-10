<template>
  <div class="flex flex-col items-center justify-center p-4 sm:p-6 md:p-8 min-h-screen transition-all duration-300">
    <div class="w-full max-w-full sm:max-w-3xl">
      <h2 class="text-2xl sm:text-3xl md:text-4xl font-semibold text-darkBlue mb-6 sm:mb-8 md:mb-10 text-center">
        Благотворительные Организации
      </h2>
      <div v-if="organizations.length" class="space-y-4 sm:space-y-6">
        <Post 
          v-for="org in organizations" 
          :key="org.id" 
          :post="org" 
        />
      </div>
      <div v-else class="text-center text-gray-500 text-sm sm:text-base">
        Нет доступных организаций для поддержки.
      </div>
    </div>

    <div class="mt-6 sm:mt-8 md:mt-10 w-full max-w-full sm:max-w-3xl">
      <Menu :goBack="goBack" :openModal="openModal" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue';
import { useRouter } from 'vue-router';
import Post from './Post.vue';
import Menu from './Menu.vue';

const organizations = ref([]);

const router = useRouter();

const goBack = () => {
  router.back();
};

const openModal = () => {
  console.log('Открыть модальное окно');
};

onMounted(async () => {
  try {
    const response = await fetch('/api/charity_organizations');
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
.text-darkBlue {
  color: #1E3A8A;
}
</style>
