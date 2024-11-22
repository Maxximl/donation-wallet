<template>
  <div class="flex-1 mb-6 flex flex-col">
    <div
      v-if="isLoading"
      class="text-center text-gray-500"
    >
    <!-- ????? -->
      Загрузка транзакций<span class="dots">...</span>
    </div>

    <div
      v-else-if="transactions.length > 0"
      :class="['space-y-4', transactions.length > 4 ? 'overflow-y-auto' : '']"
      :style="transactions.length > 4 ? 'max-height: calc(100vh - 300px)' : 'max-height: none'"
    >
      <TransactionCard
        v-for="(transaction, index) in transactions"
        :key="`${transaction.timestamp}-${transaction.amount}-${transaction.sender_account_id}-${transaction.receiver_account_id}-${index}`"
        :transaction="transaction"
        :formatDate="formatDate"
        :formatCurrency="formatCurrency"
      />
    </div>
    
<!-- ????? -->
    <div v-else class="text-center text-gray-500">
      Загрузка транзакций<span class="dots">...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import TransactionCard from './TransactionCard.vue'

interface Transaction {
  timestamp: number
  amount: number
  sender_account_id: string
  receiver_account_id: string
}

const props = defineProps<{
  transactions: Transaction[]
  formatDate: (date: number) => string
  formatCurrency: (amount: number) => string
  isLoading?: boolean
}>()
</script>

<style scoped>
.dots::after {
  content: '';
  display: inline-block;
  animation: dots 1.5s steps(5, end) infinite;
}

@keyframes dots {
  0%, 20% {
    content: '';
  }
  40% {
    content: '.';
  }
  60% {
    content: '..';
  }
  80%, 100% {
    content: '...';
  }
}
</style>
