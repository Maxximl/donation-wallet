<template>
  <div class="menu-container">
    <button @click="navigateToTransactions" class="menu-button">
      <ArrowsRightLeftIcon class="w-6 h-6 mr-2" />
      <span>Переводы</span>
    </button>
    <button @click="navigateToOrganizations" class="menu-button">
      <BuildingOfficeIcon class="w-6 h-6 mr-2" />
      <span>Организации</span>
    </button>
    <button @click="navigateToProfile" class="menu-button">
      <UserCircleIcon class="w-6 h-6 mr-2" />
      <span>Профиль</span>
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { BuildingOfficeIcon, ArrowsRightLeftIcon, UserCircleIcon } from '@heroicons/vue/24/outline';

const router = useRouter();

const navigateToOrganizations = () => {
  router.push('/posts'); 
};

const navigateToTransactions = () => {
  router.push('/transactions'); 
};

const navigateToProfile = () => {
  router.push('/profile'); 
};
</script>

<style scoped>
.menu-container {
  @apply flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0;
}

.menu-button {
  @apply flex items-center bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
}

.menu-button span {
  @apply text-base font-medium;
}
</style>
