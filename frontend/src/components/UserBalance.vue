<template>
  <div class="flex items-center bg-gradient-to-r from-blue-500 to-blue-700 text-white p-4 rounded-lg shadow-lg">
    <svg
      class="w-6 h-6 mr-3"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 8c-1.657 0-3 1.343-3 3s1.343 3 3 3 3-1.343 3-3-1.343-3-3-3zM6.343 6.343A8 8 0 1117.657 17.657 8 8 0 016.343 6.343z"
      ></path>
    </svg>
    <div>
      <p class="text-xs sm:text-sm">Баланс пользователя</p>
      <p class="text-md sm:text-lg font-semibold">{{ formattedBalance }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue';

interface Props {
  balance: number;
  formatCurrency: (value: number) => string;
}

const props = defineProps<Props>();

const formattedBalance = computed(() => props.formatCurrency(props.balance));
</script>

<style scoped>

div:hover {
  transform: scale(1.05);
  transition: transform 0.3s;
}
</style>
