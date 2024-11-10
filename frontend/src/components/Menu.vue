<template>
  <div class="menu-wrapper">
    <div class="menu-container">
      <button @click="logout" class="menu-button">
        <ArrowLeftOnRectangleIcon class="w-6 h-6 mr-2" />
        <span>Выход</span>
      </button>
      <button @click="navigateToOrganizations" class="menu-button">
        <BuildingOfficeIcon class="w-6 h-6 mr-2" />
        <span>Организации</span>
      </button>
      <!-- <button class="menu-button disabled-button" disabled>
        <UserCircleIcon class="w-6 h-6 mr-2" />
        <span>Профиль</span>
      </button> -->
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { BuildingOfficeIcon, ArrowLeftOnRectangleIcon, UserCircleIcon } from '@heroicons/vue/24/outline';

const router = useRouter();

const navigateToOrganizations = () => {
  router.push('/posts'); 
};

const logout = () => {
  router.push('/'); 
};
</script>

<style scoped>
.menu-wrapper {
  @apply w-full overflow-x-auto; 
}

.menu-container {
  @apply flex flex-col sm:flex-row flex-wrap justify-start sm:justify-between items-center space-y-4 sm:space-y-0 space-x-0 sm:space-x-4;
}

.menu-button {
  @apply flex items-center bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto transition duration-200;
}

.menu-button span {
  @apply text-base font-medium;
}

.disabled-button {
  @apply bg-gray-400 cursor-not-allowed opacity-70;
}

.disabled-button:hover {
  @apply bg-gray-400;
}
</style>
