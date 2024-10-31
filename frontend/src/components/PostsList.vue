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

onMounted(() => {
  organizations.value = [
    {
      id: 1,
      name: 'Помощь детям',
      description: 'Организация, предоставляющая поддержку детям из неблагополучных семей.',
      fundingGoal: 50000,
      currentFunding: 15000,
      author: 'Иван Иванов',
      date: '01.04.2024',
    },
    {
      id: 2,
      name: 'Здоровье для всех',
      description: 'Благотворительная организация, занимающаяся медицинской помощью нуждающимся.',
      fundingGoal: 75000,
      currentFunding: 30000,
      author: 'Мария Петрова',
      date: '15.04.2024',
    },
    {
      id: 3,
      name: 'Экология Земли',
      description: 'Организация, работающая над сохранением окружающей среды и природных ресурсов.',
      fundingGoal: 60000,
      currentFunding: 45000,
      author: 'Алексей Смирнов',
      date: '20.04.2024',
    },
  ];
});

// const handleDonate = ({ id, amount }) => {
//   const org = organizations.value.find(o => o.id === id);
//   if (org) {
//     org.currentFunding += amount;
//   }
// };

provide('organizations', organizations);
// provide('handleDonate', handleDonate);
</script>

<style scoped>
</style>
