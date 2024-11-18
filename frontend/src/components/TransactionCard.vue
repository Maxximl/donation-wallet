<template>
  <div class="transaction-card">
    <div class="flex-1">
      <p class="text-gray-600">{{ formatDate(transaction.timestamp) }}</p>
      <p class="font-medium">{{ truncatedDescription }}</p>
    </div>
    <div class="flex items-center mt-2 sm:mt-0">
      <span
        :class="{
          'text-green-600': transaction.transaction_type === 'donation',
          'text-red-600': transaction.transaction_type === 'deposit',
        }"
        class="transaction-amount mr-4"
      >
        {{ transaction.transaction_type === 'donation' ? '+' : '-' }}{{ formatAmountWithSuffix(transaction.amount) }}
      </span>
    </div>
  </div>
</template>


<script setup>
import { computed } from 'vue'

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


const formatAmountWithSuffix = (amount) => {
  const absAmount = Math.abs(amount);
  if (absAmount >= 1_000_000_000_000_000_000_000_000_000_000) return (amount / 1_000_000_000_000_000_000_000_000_000_000).toFixed(1) + 'Септ';
  if (absAmount >= 1_000_000_000_000_000_000_000_000_000) return (amount / 1_000_000_000_000_000_000_000_000_000).toFixed(1) + 'Секст';
  if (absAmount >= 1_000_000_000_000_000_000_000_000) return (amount / 1_000_000_000_000_000_000_000_000).toFixed(1) + 'Квинт';
  if (absAmount >= 1_000_000_000_000_000_000_000) return (amount / 1_000_000_000_000_000_000_000).toFixed(1) + 'Квадр';
  if (absAmount >= 1_000_000_000_000_000_000) return (amount / 1_000_000_000_000_000_000).toFixed(1) + 'Трлн';
  if (absAmount >= 1_000_000_000_000_000) return (amount / 1_000_000_000_000_000).toFixed(1) + 'Квдрлн';
  if (absAmount >= 1_000_000_000_000) return (amount / 1_000_000_000_000).toFixed(1) + 'Трлн';
  if (absAmount >= 1_000_000_000) return (amount / 1_000_000_000).toFixed(1) + 'Млрд';
  if (absAmount >= 1_000_000) return (amount / 1_000_000).toFixed(1) + 'Млн';
  if (absAmount >= 1_000) return (amount / 1_000).toFixed(1) + 'Тыс';
  return amount.toString();
}


const truncatedDescription = computed(() => {
  return props.transaction.description.length > 30
    ? props.transaction.description.slice(0, 27) + '...'
    : props.transaction.description
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
