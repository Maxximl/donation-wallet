<template>
  <div class="relative min-h-screen bg-white transition-all duration-300">
    <div>
      <div v-if="isBalanceLoading" class="loading-animation">
        <span>Загрузка баланса...</span>
      </div>
      <UserBalance
        v-else
        :balance="userBalance"
        :formatCurrency="formatCurrency"
      />
    </div>
    
    <div class="flex flex-col items-center justify-center p-4 sm:p-6 md:p-8">
  
      <div class="w-full max-w-full sm:max-w-3xl mb-6 sm:mb-8 md:mb-10">
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
            :userBalance="userBalance" 
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
    
  </div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Post from './Post.vue';
import Menu from './Menu.vue';
import UserBalance from './UserBalance.vue';

interface Organization {
  id: number;
  name: string;
  description: string;
}

const organizations = ref<Organization[]>([]);
const isLoading = ref(true);

const router = useRouter();

const goBack = () => {
  router.back();
};

const openModal = () => {
  // console.log('Открыть модальное окно');
};

const BASE_BALANCE = 1000000;

const userBalance = ref<number | null>(null);
const isBalanceLoading = ref(true);

const formatCurrency = (value: number): string => {
  // console.log('Форматирование валюты для значения:', value);
  // console.time('formatCurrency');
  const formatted = new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
  }).format(value);
  console.timeEnd('formatCurrency');
  return formatted;
};

interface Transaction {
  sender_account_id: number;
  receiver_account_id: number;
  amount: number;
  description: string;
  timestamp: string;
  transaction_type: string;
}

const transactions = ref<Transaction[]>([]);

const calculateTotalDonations = (): number => {
  const totalDonations = transactions.value
    .filter((tx) => tx.transaction_type === 'donation')
    .reduce((sum, tx) => sum + tx.amount, 0);
  return totalDonations;
};

const updateBalance = () => {
  const totalDonations = calculateTotalDonations();
  // console.log('Total Donations:', totalDonations);
  userBalance.value = BASE_BALANCE - totalDonations;
  // console.log('Баланс обновлён:', userBalance.value);
  isBalanceLoading.value = false;
};

const loadTransactionsAndUpdateBalance = async () => {
  isBalanceLoading.value = true;
  const accountId = 1;
  const transactionsSuccess = await fetchTransactions(accountId); 
  if (transactionsSuccess) {
    updateBalance();
  } else {
    console.error('Не удалось загрузить транзакции для обновления баланса');
    isBalanceLoading.value = false; 
  }
};

const fetchTransactions = async (accountId: number, timeout = 5000): Promise<boolean> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => {
    controller.abort();
  }, timeout);

  try {
    const response = await fetch(`/api/accounts/${accountId}/transactions`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error('Сетевая ошибка: ' + response.statusText);
    }

    const data = await response.json();
    // console.log('Received transactions:', data); 

    if (Array.isArray(data)) {
      transactions.value = data;
      // console.log('Транзакции сохранены:', transactions.value); 
      return true;
    } else {
      throw new Error('Полученные данные имеют неверный формат');
    }
  } catch (error: any) {
    if (error.name === 'AbortError') {
      console.warn('Запрос был прерван из-за тайм-аута');
    } else {
      console.error('Ошибка при получении данных:', error);
    }
    return false;
  }
};

const fetchOrganizations = async (timeout = 5000): Promise<Organization[] | null> => {
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
    // console.log('Received organizations:', data); 

    if (Array.isArray(data) && data.every(item => item.id && item.name && item.description)) {
      const simplifiedData: Organization[] = data.map(org => ({
        id: org.id,
        name: org.name,
        description: org.description,
      }));
      
      return simplifiedData;
    } else {
      throw new Error('Полученные данные имеют неверный формат');
    }
  } catch (error: any) {
    if (error.name === 'AbortError') {
      console.warn('Запрос был прерван из-за тайм-аута');
    } else {
      console.error('Ошибка при получении данных:', error);
    }
    return null;
  }
};

const loadOrganizations = async () => {
  isLoading.value = true;

  const cachedData = localStorage.getItem('organizations');
  if (cachedData) {
    try {
      const parsedData: Organization[] = JSON.parse(cachedData);
      organizations.value = parsedData;
      // console.log('Организации загружены из кеша');
    } catch (e) {
      console.error('Ошибка при разборе кешированных данных:', e);
      localStorage.removeItem('organizations');
    }
    isLoading.value = false;
  } else {
    // console.log('Кешированных данных нет');
    const initialTimeout = 5000; 
    const maxRetries = 5;        
    const backoffFactor = 2;  

    let timeout = initialTimeout;
    let success = false;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      // console.log(`Попытка ${attempt} с таймаутом ${timeout} мс`);
      const fetchedData = await fetchOrganizations(timeout);
      if (fetchedData) {
        organizations.value = fetchedData;
        localStorage.setItem('organizations', JSON.stringify(fetchedData));
        // console.log('Данные успешно получены с сервера и сохранены в кеш');
        success = true;
        break;
      } else {
        console.warn(`Попытка ${attempt} не удалась`);
        timeout *= backoffFactor; 
      }
    }

    if (!success) {
      console.warn('Не удалось получить данные с сервера, и кешированные данные отсутствуют');
    }

    isLoading.value = false;
  }

  await loadTransactionsAndUpdateBalance();
};

onMounted(() => {
  loadOrganizations();
});

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

.loading-animation {
  text-align: center;
  font-size: 1.2em;
  color: #1E3A8A;
}
</style>
