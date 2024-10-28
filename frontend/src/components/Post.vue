<template>
  <div class="card">
    <img 
      v-if="post.image" 
      :src="post.image" 
      alt="Изображение организации" 
      class="image"
    >
    <h3 class="title">{{ post.name }}</h3>
    <p class="description">{{ post.description }}</p>
    
    <div class="funding-section">
      <div class="funding-info">
        <span class="label">Цель финансирования:</span>
        <span class="amount">{{ formatCurrency(post.fundingGoal) }}</span>
      </div>
      <div class="progress-bar">
        <div 
          class="progress" 
          :style="{ width: fundingPercentage + '%' }"
        ></div>
      </div>
      <div class="current-funding">
        <span>Собрано:</span>
        <span>{{ formatCurrency(post.currentFunding) }}</span>
      </div>
    </div>
    
    <button @click="donate" class="donate-button">
      Пожертвовать
    </button>
    
    <div class="footer">
      <span>Автор: {{ post.author }}</span>
      <span>{{ post.date }}</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed, defineEmits } from 'vue';

const props = defineProps({
  post: {
    type: Object,
    required: true,
    default: () => ({
      id: null,
      name: '',
      description: '',
      image: '',
      fundingGoal: 0,
      currentFunding: 0,
      author: '',
      date: '',
    }),
  },
});

const emit = defineEmits(['donate']);

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value);
};

const fundingPercentage = computed(() => {
  if (props.post.fundingGoal === 0) return 0;
  const percentage = (props.post.currentFunding / props.post.fundingGoal) * 100;
  return percentage > 100 ? 100 : percentage.toFixed(2);
});

const donate = () => {
  const donationAmount = 1000;
  alert(`Спасибо за пожертвование в размере ${formatCurrency(donationAmount)}!`);
  emit('donate', { id: props.post.id, amount: donationAmount });
};
</script>

<style scoped>
.card {
  @apply bg-white p-6 rounded-3xl shadow-lg w-full max-w-lg transform transition-transform hover:scale-105;
}

.image {
  @apply w-full h-48 object-cover rounded-lg mb-4;
}

.title {
  @apply text-2xl font-semibold text-darkBlue mb-2;
}

.description {
  @apply text-gray-700 mb-4;
}

.funding-section {
  @apply mb-4;
}

.funding-info {
  @apply flex justify-between items-center;
}

.label {
  @apply text-muted;
}

.amount {
  @apply text-darkBlue;
}

.progress-bar {
  @apply w-full bg-gray-200 rounded-full h-4 mt-1;
}

.progress {
  @apply bg-primary h-4 rounded-full;
}

.current-funding {
  @apply flex justify-between items-center text-sm text-muted mt-1;
}

.donate-button {
  @apply w-full bg-accent text-white py-2 px-4 rounded-lg transition-all;
}

.footer {
  @apply flex justify-between items-center text-sm text-muted mt-4;
}

.text-muted {
  color: #566bb7;
}
.bg-primary {
  background-color: #3b82f6; 
}
.bg-accent {
  background-color: #3b82f6; 
}
.text-darkBlue {
  color: #1e40af; 
}
</style>