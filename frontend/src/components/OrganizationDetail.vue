<template>
  <div class="flex flex-col p-4 min-h-screen">
    <div class="max-w-4xl mx-auto flex flex-col flex-1 space-y-4">
      <OrganizationHeader :organization="organization" />

      <h2 class="text-2xl font-semibold text-darkBlue mb-2 text-center">
        Транзакции:
      </h2>
   
      <TransactionList
        :transactions="mergedTransactions"
        :formatDate="formatDate"
        :formatCurrency="formatCurrency"
      />
 
      <button @click="openModal" class="donate-button my-6">
        Отправить пожертвование
      </button>
    
      <Menu :goBack="goBack" :openModal="openModal" />

      <!-- 
      <div v-if="isLoading" class="text-center text-gray-500 mt-4">
        Загрузка транзакций...
      </div>
      <div v-if="error" class="text-center text-red-500 mt-4">
        {{ error }}
      </div>
      -->
    </div>

    <DonationModal
      v-if="isModalOpen"
      :isModalOpen="isModalOpen"
      :predefinedAmounts="predefinedAmounts"
      :formatCurrency="formatCurrency"
      :isSubmitting="isSubmitting"
      @close-modal="closeModal"
      @submit-donation="submitDonation"
    />
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  computed,
  watch,
  onBeforeUnmount,
  defineProps,
} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import OrganizationHeader from './OrganizationHeader.vue';
import TransactionList from './TransactionList.vue';
import Menu from './Menu.vue';
import DonationModal from './DonationModal.vue';
// import UserBalance from './UserBalance.vue'; // Импортируем компонент

const props = defineProps<{ userBalance: number }>();

interface Transaction {
  sender_account_id: number;
  receiver_account_id: number;
  amount: number;
  description: string;
  timestamp: string;
  transaction_type: string;
}

interface Organization {
  id: number | null;
  name: string;
  description: string;
  website: string;
  email: string;
  phone_number: string;
  address: string;
  account_id: number;
  incomingTransactions: Transaction[];
  outgoingTransactions: Transaction[];
}

const route = useRoute();
const router = useRouter();

const organization = ref<Organization>({
  id: null,
  name: '',
  description: '',
  website: '',
  email: '',
  phone_number: '',
  address: '',
  account_id: 0,
  incomingTransactions: [],
  outgoingTransactions: [],
});

const isModalOpen = ref(false);
const predefinedAmounts = ref<number[]>([500, 1000, 2000, 5000]);

const isLoading = ref(true);
const error = ref<string | null>(null);
const pollingInterval = ref<number | null>(null);

const isSubmitting = ref(false);

const getCacheKey = (id: number): string => `organization_${id}`;

const loadCachedOrganization = (id: number): { name: string; description: string } | null => {
  const cacheKey = getCacheKey(id);
  const cachedData = localStorage.getItem(cacheKey);
  if (cachedData) {
    try {
      const parsedData = JSON.parse(cachedData);
      if (parsedData.name && parsedData.description) {
        // console.log(`Кешированные данные организации ${id} загружены`);
        return {
          name: parsedData.name,
          description: parsedData.description,
        };
      }
    } catch (e) {
      console.error('Ошибка при разборе кешированных данных:', e);
      localStorage.removeItem(cacheKey);
    }
  }
  return null;
};

const saveOrganizationToCache = (id: number, name: string, description: string): void => {
  const cacheKey = getCacheKey(id);
  const dataToCache = { name, description };
  localStorage.setItem(cacheKey, JSON.stringify(dataToCache));
  // console.log(`Данные организации ${id} сохранены в кеш`);
};

const openModal = (): void => {
  // console.log('Открытие модального окна пожертвования');
  isModalOpen.value = true;
};

const closeModal = (): void => {
  // console.log('Закрытие модального окна пожертвования');
  isModalOpen.value = false;
};

const submitDonation = async (donationData: {
  amount: number;
  comment: string;
}): Promise<void> => {
  if (isSubmitting.value) return;
  isSubmitting.value = true; 

  // console.log('Начало отправки пожертвования:', donationData);
  console.time('submitDonation');

  const { amount, comment } = donationData;

  if (!amount || amount < 1) {
    console.warn('Некорректная сумма пожертвования:', amount);
    isSubmitting.value = false;
    console.timeEnd('submitDonation');
    return;
  }

  const idParam = route.params.id;
  const organizationId = Array.isArray(idParam)
    ? parseInt(idParam[0], 10)
    : parseInt(idParam as string, 10);
 
  let senderId: number;
  let receiverId: number;

  if (organizationId === 1) {
    senderId = 2;
    receiverId = 1;
  } else if (organizationId === 2) {
    senderId = 1;
    receiverId = 2;
  } else {
    senderId = 1;
    receiverId = organizationId;
  }

  const newTransaction: Transaction = {
    sender_account_id: senderId,
    receiver_account_id: receiverId,
    amount: amount,
    description: comment || 'Пожертвование без комментария',
    timestamp: new Date().toISOString(),
    transaction_type: 'donation',
  };

  try {
    console.time('POST /api/accounts/transactions');
    const response = await fetch(
      `/api/accounts/${receiverId}/transactions`,
      {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newTransaction),
      }
    );
    console.timeEnd('POST /api/accounts/transactions');

    if (!response.ok) {
      console.error('Ошибка при отправке пожертвования:', response.statusText);
      return;
    }

    console.time('Добавление транзакции в состояние');
    if (
      organization.value.account_id !== null &&
      newTransaction.receiver_account_id === organization.value.account_id
    ) {
      organization.value.incomingTransactions.push(newTransaction);
      // console.log('Добавлена входящая транзакция:', newTransaction);
    }
    if (
      organization.value.account_id !== null &&
      newTransaction.sender_account_id === organization.value.account_id
    ) {
      organization.value.outgoingTransactions.push(newTransaction);
      // console.log('Добавлена исходящая транзакция:', newTransaction);
    }
    console.timeEnd('Добавление транзакции в состояние');
   
  } catch (error) {
    console.error('Ошибка при отправке пожертвования:', error);
  } finally {
    closeModal();
    isSubmitting.value = false;
    console.timeEnd('submitDonation');
  }
};

const formatCurrency = (value: number): string => {
  // console.log('Форматирование валюты для значения:', value);
  console.time('formatCurrency');
  const formatted = new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
  }).format(value);
  console.timeEnd('formatCurrency');
  return formatted;
};

const formatDate = (dateStr: string): string => {
  // console.log('Форматирование даты для строки:', dateStr);
  console.time('formatDate');
  if (!dateStr) return '';
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return 'Некорректная дата';
  const formatted = date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
  console.timeEnd('formatDate');
  return formatted;
};

const goBack = (): void => {
  // console.log('Возврат на предыдущую страницу');
  router.back();
};

const mergedTransactions = computed<Transaction[]>(() => {
  // console.log('Вычисление mergedTransactions');
  // console.time('mergedTransactions Computation');

  const idParam = route.params.id;
  const organizationId = Array.isArray(idParam)
    ? parseInt(idParam[0], 10)
    : parseInt(idParam as string, 10);

  const transactionSet = new Set<string>();
  const uniqueTransactions: (Transaction & { timestampMillis: number })[] = [];

  const createUniqueKey = (tx: Transaction): string => {
    return `${tx.sender_account_id}-${tx.receiver_account_id}-${tx.amount}-${tx.timestamp}-${tx.description}-${tx.transaction_type}`;
  };

  const processTransactions = (transactions: Transaction[]) => {
    transactions.forEach((tx) => {
      const uniqueKey = createUniqueKey(tx);
      if (!transactionSet.has(uniqueKey)) {
        transactionSet.add(uniqueKey);
        const date = new Date(tx.timestamp);
        const timestampMillis = isNaN(date.getTime()) ? 0 : date.getTime();
        uniqueTransactions.push({
          ...tx,
          timestampMillis,
        });
      }
    });
  };

  console.time('Processing Incoming Transactions');
  processTransactions(organization.value.incomingTransactions);
  console.timeEnd('Processing Incoming Transactions');

  console.time('Processing Outgoing Transactions');
  processTransactions(organization.value.outgoingTransactions);
  console.timeEnd('Processing Outgoing Transactions');

  // Новая фильтрация на основе маршрута
  let filteredTransactions: (Transaction & { timestampMillis: number })[] = [];

  if (organizationId === 1) {
    filteredTransactions = uniqueTransactions.filter(
      (tx) =>
        tx.receiver_account_id === 1 && tx.sender_account_id === 2
    );
  } else if (organizationId === 2) {
    filteredTransactions = uniqueTransactions.filter(
      (tx) =>
        tx.receiver_account_id === 2 && tx.sender_account_id === 1
    );
  } else {
    // Если требуется обработка других ID, можно добавить дополнительные условия
    filteredTransactions = uniqueTransactions.filter(
      (tx) =>
        tx.receiver_account_id === organizationId ||
        tx.sender_account_id === organizationId
    );
  }
 
  filteredTransactions.sort((a, b) => b.timestampMillis - a.timestampMillis);

  console.timeEnd('mergedTransactions Computation');
  return filteredTransactions;
});

const fetchOrganizationData = async (id: number): Promise<void> => {
  // console.log(`Начало загрузки данных для организации ID: ${id}`);
  // console.time('fetchOrganizationData');

  isLoading.value = true;
  error.value = null;

  const cachedOrg = loadCachedOrganization(id);
  if (cachedOrg) {
    organization.value.name = cachedOrg.name;
    organization.value.description = cachedOrg.description;
  }

  try {
    console.time('Параллельные запросы к API');
    const [organizationResponse, transactionsResponse] = await Promise.all([
      fetch(`/api/charity_organizations/${id}`, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      }),
      fetch(`/api/accounts/1/transactions`, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      }),
    ]);
    console.timeEnd('Параллельные запросы к API');

    if (!organizationResponse.ok) {
      throw new Error('Ошибка при получении данных организации');
    }
    if (!transactionsResponse.ok) {
      throw new Error('Ошибка при получении транзакций');
    }

    console.time('Парсинг данных организации');
    const orgData = (await organizationResponse.json()) as Organization;
    console.timeEnd('Парсинг данных организации');

    // console.log('Найдена организация:', orgData);
    organization.value = {
      ...organization.value, 
      id: orgData.id,
      name: orgData.name, 
      description: orgData.description,
      website: orgData.website,
      email: orgData.email,
      phone_number: orgData.phone_number,
      address: orgData.address,
      account_id: orgData.account_id,
      incomingTransactions: [],
      outgoingTransactions: [],
    };

    saveOrganizationToCache(id, orgData.name, orgData.description);

    console.time('Парсинг транзакций');
    let transactionsData = (await transactionsResponse.json()) as Transaction[];
    console.timeEnd('Парсинг транзакций');

    transactionsData = transactionsData.filter(
      (tx) =>
        tx.receiver_account_id === organization.value.account_id ||
        tx.sender_account_id === organization.value.account_id
    );

    organization.value.incomingTransactions = transactionsData.filter(
      (tx) => tx.receiver_account_id === organization.value.account_id
    );
    organization.value.outgoingTransactions = transactionsData.filter(
      (tx) => tx.sender_account_id === organization.value.account_id
    );

    // console.log(
    //   'Incoming Transactions:',
    //   JSON.stringify(organization.value.incomingTransactions, null, 2)
    // );
    // console.log(
    //   'Outgoing Transactions:',
    //   JSON.stringify(organization.value.outgoingTransactions, null, 2)
    // );
  } catch (err) {
    console.error('Ошибка при загрузке данных организации:', err);
    error.value = (err as Error).message;
  } finally {
    isLoading.value = false;
    console.timeEnd('fetchOrganizationData');
  }
};

const fetchTransactions = async (): Promise<void> => {
  // console.log('Начало обновления транзакций');
  // console.time('fetchTransactions');

  try {
    const idParam = route.params.id;
    const organizationId = Array.isArray(idParam)
      ? parseInt(idParam[0], 10)
      : parseInt(idParam as string, 10);

    const transactionsResponse = await fetch(
      `/api/accounts/${organizationId}/transactions`,
      {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      }
    );

    if (!transactionsResponse.ok) {
      throw new Error('Ошибка при получении транзакций');
    }

    const transactionsData = (await transactionsResponse.json()) as Transaction[];

    const filteredTransactions = transactionsData.filter(
      (tx) =>
        tx.receiver_account_id === organization.value.account_id ||
        tx.sender_account_id === organization.value.account_id
    );

    organization.value.incomingTransactions = filteredTransactions.filter(
      (tx) => tx.receiver_account_id === organization.value.account_id
    );
    organization.value.outgoingTransactions = filteredTransactions.filter(
      (tx) => tx.sender_account_id === organization.value.account_id
    );

    // console.log('Транзакции обновлены:', filteredTransactions);

  } catch (err) {
    console.error('Ошибка при обновлении транзакций:', err);
  } finally {
    console.timeEnd('fetchTransactions');
  }
};

onMounted(() => {
  const idParam = route.params.id;
  const id = Array.isArray(idParam)
    ? parseInt(idParam[0], 10)
    : parseInt(idParam as string, 10);
  // console.log('Компонент смонтирован с ID:', id);
  fetchOrganizationData(id).then(() => {
    if (organization.value.incomingTransactions.length > 0) {
      // console.log(
      //   'Пример входящей транзакции:',
      //   JSON.stringify(organization.value.incomingTransactions[0], null, 2)
      // );
    } else {
      // console.log('Нет входящих транзакций для примера');
    }
  });

  pollingInterval.value = window.setInterval(() => {
    fetchTransactions();
  }, 3000);
});

onBeforeUnmount(() => {
  if (pollingInterval.value !== null) {
    clearInterval(pollingInterval.value);
    // console.log('Polling остановлен');
  }
});

watch(
  () => route.params.id,
  (newId, oldId) => {
    // console.log(`Изменение ID организации: старое=${oldId}, новое=${newId}`);
    if (newId !== oldId) {
      const idParam = newId;
      const parsedId = Array.isArray(idParam)
        ? parseInt(idParam[0], 10)
        : parseInt(idParam as string, 10);
      // console.log(
      //   `Перезагрузка данных для новой организации ID: ${parsedId}`
      // );
      fetchOrganizationData(parsedId);

      if (pollingInterval.value !== null) {
        clearInterval(pollingInterval.value);
        // console.log('Старый polling остановлен из-за смены ID организации');
      }
      pollingInterval.value = window.setInterval(() => {
        fetchTransactions();
      }, 3000);
    }
  }
);
</script>

<style scoped>
.text-darkBlue {
  color: #1E3A8A;
}

.donate-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto transition duration-300 ease-in-out;
}

.donate-button:focus {
  @apply outline-none ring-2 ring-blue-300;
}
</style>
