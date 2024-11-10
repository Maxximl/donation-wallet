<template>
  <div class="flex-1 mb-6 flex flex-col">
    <div
      v-if="transactions.length > 0"
      :class="['space-y-4', transactions.length > 4 ? 'overflow-y-auto' : '']"
      :style="transactions.length > 4 ? 'max-height: calc(100vh - 300px)' : 'max-height: none'"
    >
      <TransactionCard
        v-for="(transaction, index) in transactions"
        :key="index"
        :transaction="transaction"
        :formatDate="formatDate"
        :formatCurrency="formatCurrency"
      />
    </div>

    <div v-else class="text-center text-gray-500">
      Нет транзакций для отображения.
    </div>
  </div>
</template>

<script setup>
import TransactionCard from './TransactionCard.vue'

defineProps({
  transactions: {
    type: Array,
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
