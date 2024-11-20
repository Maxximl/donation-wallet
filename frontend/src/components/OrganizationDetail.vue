<template>
  <div class="flex flex-col p-4">
    <div class="max-w-3xl mx-auto flex flex-col flex-1">
      <OrganizationHeader :organization="organization" />

      <h2 class="text-2xl font-semibold text-darkBlue mb-4 text-center">
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

      <!-- <div v-if="isLoading" class="text-center text-gray-500 mt-4">
        Загрузка транзакций...
      </div> -->
      <!-- <div v-if="error" class="text-center text-red-500 mt-4">
        {{ error }}
      </div> -->
    </div>

    <DonationModal
      v-if="isModalOpen"
      :is-modal-open="isModalOpen"
      :predefined-amounts="predefinedAmounts"
      :format-currency="formatCurrency"
      @close-modal="closeModal"
      @submit-donation="submitDonation"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import OrganizationHeader from './OrganizationHeader.vue';
import TransactionList from './TransactionList.vue';
import Menu from './Menu.vue';
import DonationModal from './DonationModal.vue';

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
  account_id: number | null;
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
  account_id: null,
  incomingTransactions: [],
  outgoingTransactions: [],
});

const isModalOpen = ref(false);
const predefinedAmounts = ref<number[]>([500, 1000, 2000, 5000]);
const isLoading = ref(true);
const error = ref<string | null>(null);

const openModal = (): void => {
  console.log('Открытие модального окна пожертвования');
  isModalOpen.value = true;
};

const closeModal = (): void => {
  console.log('Закрытие модального окна пожертвования');
  isModalOpen.value = false;
};

const submitDonation = async (donationData: { amount: number; comment: string }): Promise<void> => {
  console.log('Начало отправки пожертвования:', donationData);
  console.time('submitDonation');
  
  const { amount, comment } = donationData;

  if (!amount || amount < 1) {
    console.warn('Некорректная сумма пожертвования:', amount);
    console.timeEnd('submitDonation');
    return;
  }

  const organizationId = parseInt(route.params.id as string, 10);

  const newTransaction: Transaction = {
    sender_account_id: 1,
    receiver_account_id: organizationId,
    amount: amount,
    description: comment || 'Пожертвование без комментария',
    timestamp: new Date().toISOString(),
    transaction_type: 'donation',
  };

  try {
    console.time('POST /api/accounts/transactions');
    const response = await fetch(`/api/accounts/${organizationId}/transactions`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTransaction),
    });
    console.timeEnd('POST /api/accounts/transactions');

    if (!response.ok) {
      console.error('Ошибка при отправке пожертвования:', response.statusText);
      return;
    }

    console.time('Добавление транзакции в состояние');
    if (newTransaction.receiver_account_id === organization.value.account_id) {
      organization.value.incomingTransactions.push(newTransaction);
      console.log('Добавлена входящая транзакция:', newTransaction);
    }
    if (newTransaction.sender_account_id === organization.value.account_id) {
      organization.value.outgoingTransactions.push(newTransaction);
      console.log('Добавлена исходящая транзакция:', newTransaction);
    }
    console.timeEnd('Добавление транзакции в состояние');
  } catch (error) {
    console.error('Ошибка при отправке пожертвования:', error);
  } finally {
    closeModal();
    console.timeEnd('submitDonation');
  }
};

const formatCurrency = (value: number): string => {
  console.log('Форматирование валюты для значения:', value);
  console.time('formatCurrency');
  const formatted = new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value);
  console.timeEnd('formatCurrency');
  return formatted;
};

const formatDate = (dateStr: string): string => {
  console.log('Форматирование даты для строки:', dateStr);
  console.time('formatDate');
  if (!dateStr) return '';
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return dateStr;
  const formatted = date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
  console.timeEnd('formatDate');
  return formatted;
};

const goBack = (): void => {
  console.log('Возврат на предыдущую страницу');
  router.back();
};

const mergedTransactions = computed<Transaction[]>(() => {
  console.log('Вычисление mergedTransactions');
  console.time('mergedTransactions Computation');
  
  const organizationId = parseInt(route.params.id as string, 10);

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
        uniqueTransactions.push({
          ...tx,
          timestampMillis: new Date(tx.timestamp).getTime(),
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

  const filteredTransactions = uniqueTransactions.filter(
    (tx) => tx.receiver_account_id === organizationId || tx.sender_account_id === organizationId
  );

  filteredTransactions.sort((a, b) => b.timestampMillis - a.timestampMillis);

  console.timeEnd('mergedTransactions Computation');
  return filteredTransactions;
});

watch(mergedTransactions, (newVal) => {
  console.log('Merged Transactions изменились:', JSON.stringify(newVal, null, 2));
});

const fetchOrganizationData = async (id: number): Promise<void> => {
  console.log(`Начало загрузки данных для организации ID: ${id}`);
  console.time('fetchOrganizationData');

  isLoading.value = true;
  error.value = null;

  try {
    console.time('Параллельные запросы к API');
    const [organizationResponse, transactionsResponse] = await Promise.all([
      fetch(`/api/charity_organizations/${id}`, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      }),
      fetch(`/api/accounts/${id}/transactions`, {
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

    console.log('Найдена организация:', orgData);
    organization.value = {
      ...orgData,
      incomingTransactions: [],
      outgoingTransactions: [],
    };

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

    // Логирование транзакций
    console.log(
      'Incoming Transactions:',
      JSON.stringify(organization.value.incomingTransactions, null, 2)
    );
    console.log(
      'Outgoing Transactions:',
      JSON.stringify(organization.value.outgoingTransactions, null, 2)
    );
  } catch (err) {
    console.error('Ошибка при загрузке данных организации:', err);
    error.value = (err as Error).message;
  } finally {
    isLoading.value = false;
    console.timeEnd('fetchOrganizationData');
  }
};



onMounted(() => {
  const id = parseInt(route.params.id as string, 10);
  console.log('Компонент смонтирован с ID:', id);
  fetchOrganizationData(id).then(() => {
    if (organization.value.incomingTransactions.length > 0) {
      console.log(
        'Пример входящей транзакции:',
        JSON.stringify(organization.value.incomingTransactions[0], null, 2)
      );
    } else {
      console.log('Нет входящих транзакций для примера');
    }
  });
});

console.log('Organization ID:', route.params.id);

watch(
  () => route.params.id,
  (newId, oldId) => {
    console.log(`Изменение ID организации: старое=${oldId}, новое=${newId}`);
    if (newId !== oldId) {
      const parsedId = parseInt(newId as string, 10);
      console.log(`Перезагрузка данных для новой организации ID: ${parsedId}`);
      fetchOrganizationData(parsedId);
    }
  }
);
</script>

<style scoped>
.text-darkBlue {
  color: #1E3A8A;
}

.donate-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
}
</style>
