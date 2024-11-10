<template>
    <div class="transaction-card">
      <div class="flex-1">
        <p class="text-gray-600">{{ formatDate(transaction.timestamp) }}</p>
        <p class="font-medium">{{ transaction.description }}</p>
      </div>
      <div class="flex items-center mt-2 sm:mt-0">
        <span
          :class="{
            'text-green-600': transaction.transaction_type === 'donation',
            'text-red-600': transaction.transaction_type === 'deposit',
          }"
          class="transaction-amount mr-4"
        >
          {{ transaction.transaction_type === 'donation' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
        </span>
        <span class="text-sm text-gray-500">{{ transaction.comment }}</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    transaction: {
      type: Object,
      required: true,
    },
    formatDate: {
      type: Function,
      required: true,
    },
    formatCurrency: {
      type: Function,
      required: true,
    },
  })
  </script>
  
  <style scoped>
  .transaction-card {
    @apply flex flex-col sm:flex-row justify-between items-start sm:items-center p-4 bg-white shadow rounded-lg;
  }
  
  .transaction-amount {
    @apply font-semibold mr-4;
  }
  </style>