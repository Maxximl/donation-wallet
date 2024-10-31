<template>
  <div class="card">
    <router-link 
      :to="{ name: 'OrganizationDetail', params: { id: post.id } }" 
      class="block"
    >
      <img 
        v-if="post.image" 
        :src="post.image" 
        alt="Изображение организации" 
        class="image"
      >
      <h3 class="title">{{ post.name }}</h3>
      <p class="description">{{ post.description }}</p>
      
      <div class="footer">
        <span>Автор: {{ post.author }}</span>
        <span>{{ post.date }}</span>
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

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
</script>

<style scoped>
.card {
  @apply bg-white p-6 rounded-3xl shadow-lg w-full max-w-lg relative;
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
