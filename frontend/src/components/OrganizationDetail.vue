<template>
  <div class="flex flex-col h-screen p-4">
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
 
      <div v-if="isLoading" class="text-center text-gray-500 mt-4">
        Загрузка транзакций...
      </div>
      <div v-if="error" class="text-center text-red-500 mt-4">
        {{ error }}
      </div>
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


<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import OrganizationHeader from './OrganizationHeader.vue'
import TransactionList from './TransactionList.vue'
import Menu from './Menu.vue'
import DonationModal from './DonationModal.vue'

const route = useRoute()
const router = useRouter()

const organization = ref({
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
})

const isModalOpen = ref(false)
const predefinedAmounts = [500, 1000, 2000, 5000]
const isLoading = ref(true)
const error = ref(null)

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const submitDonation = async (donationData) => {
  let { amount, comment } = donationData;

  if (!amount || amount < 1) {
    return;
  }

  const newTransaction = {
    sender_account_id: null, 
    receiver_account_id: organization.value.account_id,
    amount: amount,
    description: comment || 'Пожертвование через интерфейс',
    timestamp: new Date().toISOString(),
    transaction_type: 'donation',
  };

  const transactionsKey = `transactions_${organization.value.account_id}`;

  try {
    const response = await fetch('/api/transactions', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTransaction),
    });

    if (!response.ok) {
      console.error('Ошибка при отправке транзакции:', response.statusText);
      return;
    }

    const createdTransaction = await response.json();
    newTransaction.id = createdTransaction.id;

    const cachedTransactions = JSON.parse(localStorage.getItem(transactionsKey)) || [];
    cachedTransactions.push(newTransaction);
    localStorage.setItem(transactionsKey, JSON.stringify(cachedTransactions));

    if (newTransaction.receiver_account_id === organization.value.account_id) {
      organization.value.incomingTransactions.push(newTransaction);
    }
    if (newTransaction.sender_account_id === organization.value.account_id) {
      organization.value.outgoingTransactions.push(newTransaction);
    }
  } catch (error) {
    console.error('Ошибка при отправке транзакции:', error);
  } finally {
    closeModal();
  }
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  if (isNaN(date)) return dateStr
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

const goBack = () => {
  router.back()
}

const mergedTransactions = computed(() => {
  const incoming = organization.value.incomingTransactions.map(tx => ({
    ...tx,
    type: 'donation',
    description: tx.description,
  }))

  const outgoing = organization.value.outgoingTransactions.map(tx => ({
    ...tx,
    type: 'deposit',
    description: tx.description,
  }))

  return [...incoming, ...outgoing].sort((a, b) => {
    const dateA = new Date(a.timestamp)
    const dateB = new Date(b.timestamp)
    return dateB - dateA
  })
})

const organizationReceiverMap = {
  1: 3, 
  2: 1, 
}

const fetchOrganizationData = async (id) => {
  isLoading.value = true
  error.value = null

  try {
    const organizationResponse = await fetch(`/api/charity_organizations/${id}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })

    if (!organizationResponse.ok) {
      throw new Error('Ошибка при получении данных организации: ' + organizationResponse.statusText)
    }

    const orgData = await organizationResponse.json()
    organization.value = {
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
    }

    const receiverAccountId = organizationReceiverMap[id]

    if (!receiverAccountId) {
      throw new Error('Receiver Account ID не найден для организации с ID: ' + id)
    }

    const transactionsKey = `transactions_${receiverAccountId}`

    const cachedTransactions = JSON.parse(localStorage.getItem(transactionsKey))

    if (cachedTransactions && cachedTransactions.length > 0) {
      organization.value.incomingTransactions = cachedTransactions.filter(
        tx => tx.receiver_account_id === receiverAccountId
      )
      organization.value.outgoingTransactions = cachedTransactions.filter(
        tx => tx.sender_account_id === organization.value.account_id
      )
    } else {
      const transactionsResponse = await fetch(`/api/accounts/${receiverAccountId}/transactions`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      })

      if (!transactionsResponse.ok) {
        throw new Error('Ошибка при получении транзакций: ' + transactionsResponse.statusText)
      }

      const transactionsData = await transactionsResponse.json()
      organization.value.incomingTransactions = transactionsData.filter(
        tx => tx.receiver_account_id === receiverAccountId
      )
      organization.value.outgoingTransactions = transactionsData.filter(
        tx => tx.sender_account_id === organization.value.account_id
      )

      localStorage.setItem(transactionsKey, JSON.stringify(transactionsData))
    }
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  const id = parseInt(route.params.id, 10)
  fetchOrganizationData(id)
})

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId !== oldId) {
      fetchOrganizationData(parseInt(newId, 10))
    }
  }
)
</script>

<style scoped>
.text-darkBlue {
  color: #1E3A8A;
}

.donate-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
}
</style>
