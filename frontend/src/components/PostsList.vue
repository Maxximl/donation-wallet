<template>
  <div class="flex flex-col items-center justify-center p-4 sm:p-6 md:p-8 min-h-screen transition-all duration-300">
    <div class="w-full max-w-full sm:max-w-3xl">
      <h2 class="text-2xl sm:text-3xl md:text-4xl font-semibold text-darkBlue mb-6 sm:mb-8 md:mb-10 text-center">
        Благотворительные Организации
      </h2>
      <div v-if="isLoading" class="text-center text-gray-500 text-sm sm:text-base">
        Загрузка организаций<span class="dots">...</span>
      </div>
      <div v-else-if="organizations.length" class="space-y-4 sm:space-y-6">
        <Post 
          v-for="org in organizations" 
          :key="org.id" 
          :post="org" 
        />
      </div>
      <div v-else class="text-center text-gray-500 text-sm sm:text-base">
        Нет доступных организаций для поддержки.
      </div>
    </div>

    <div class="mt-6 sm:mt-8 md:mt-10 w-full max-w-full sm:max-w-3xl">
      <Menu :goBack="goBack" :openModal="openModal" />
    </div>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue';
import { useRouter } from 'vue-router';
import Post from './Post.vue';
import Menu from './Menu.vue';

const organizations = ref([]);
const isLoading = ref(true);

const router = useRouter();

const goBack = () => {
  router.back();
};

const openModal = () => {
  console.log('Открыть модальное окно');
};

const fetchOrganizations = async (timeout = 5000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => {
    controller.abort();
  }, timeout);

  try {
    const response = await fetch('/api/charity_organizations', {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error('Сетевая ошибка: ' + response.statusText);
    }

    const data = await response.json();

    if (Array.isArray(data) && data.every(item => item.id && item.name)) {
      organizations.value = data;
      localStorage.setItem('organizations', JSON.stringify(data));
      return true;
    } else {
      throw new Error('Полученные данные имеют неверный формат');
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.warn('Запрос был прерван из-за тайм-аута');
    } else {
      console.error('Ошибка при получении данных:', error);
    }
    return false;
  }
};

const loadOrganizations = async () => {
  isLoading.value = true;

  const initialTimeout = 5000; 
  const maxRetries = 5;        
  const backoffFactor = 2;    

  let timeout = initialTimeout;
  let success = false;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    console.log(`Попытка ${attempt} с таймаутом ${timeout} мс`);
    success = await fetchOrganizations(timeout);
    if (success) {
      console.log('Данные успешно получены');
      break;
    } else {
      console.warn(`Попытка ${attempt} не удалась`);
      timeout *= backoffFactor; 
    }
  }

  if (!success) {
    console.warn('Все попытки не увенчались успехом, пытаемся загрузить кешированные данные');
    const cachedData = localStorage.getItem('organizations');
    if (cachedData) {
      organizations.value = JSON.parse(cachedData);
    } else {
      console.error('Кешированных данных нет');
    }
  }

  isLoading.value = false;
};

loadOrganizations();

provide('organizations', organizations);
</script>

<style scoped>
.text-darkBlue {
  color: #1E3A8A;
}

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
