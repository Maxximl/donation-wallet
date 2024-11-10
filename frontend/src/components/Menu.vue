<template>
    <div class="menu-container">
      <button @click="goBack" class="menu-button">
        Назад
      </button>
      <button @click="openModal" class="menu-button">
        Отправить пожертвование
      </button>
    </div>
  </template>
  
  <script setup>
  defineProps({
    goBack: {
      type: Function,
      required: true,
    },
    openModal: {
      type: Function,
      required: true,
    },
  })
  </script>
  
  <style scoped>
  .menu-container {
    @apply flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0;
  }
  
  .menu-button {
    @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
  }
  </style>
  