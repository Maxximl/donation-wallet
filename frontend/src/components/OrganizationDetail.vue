
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

      <Menu :goBack="goBack" :openModal="openModal" />
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
import { ref, onMounted, computed } from 'vue'
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

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const submitDonation = async (donationData) => {
  let { amount, comment } = donationData

  if (!amount || amount < 1) {
    return
  }

  const newTransaction = {
    sender_account_id: organization.value.account_id,
    receiver_account_id: organization.value.account_id,
    amount: amount,
    description: comment,
    timestamp: new Date().toISOString(),
    transaction_type: 'donation',
  }

  const transactionsKey = `transactions_${organization.value.account_id}`

  const cachedTransactions = JSON.parse(localStorage.getItem(transactionsKey)) || []
  cachedTransactions.push(newTransaction)
  localStorage.setItem(transactionsKey, JSON.stringify(cachedTransactions))

  const response = await fetch('http://localhost:8000/api/transactions', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newTransaction),
  })

  if (!response.ok) {
    return
  }

  const createdTransaction = await response.json()
  organization.value.incomingTransactions.push({
    ...newTransaction,
    id: createdTransaction.id,
  })

  cachedTransactions[cachedTransactions.length - 1].id = createdTransaction.id
  localStorage.setItem(transactionsKey, JSON.stringify(cachedTransactions))

  closeModal()
}

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

onMounted(async () => {
  const id = parseInt(route.params.id, 10)
  const organizationResponse = await fetch(`http://localhost:8000/api/charity_organizations/${id}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  })

  if (!organizationResponse.ok) {
    console.warn('Ошибка при получении данных организации:', organizationResponse.statusText)
    return
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

  const transactionsKey = `transactions_${organization.value.account_id}`

  const cachedTransactions = JSON.parse(localStorage.getItem(transactionsKey))

  if (cachedTransactions && cachedTransactions.length > 0) {
    organization.value.incomingTransactions = cachedTransactions.filter(
      tx => tx.receiver_account_id === orgData.account_id
    )
    organization.value.outgoingTransactions = cachedTransactions.filter(
      tx => tx.sender_account_id === orgData.account_id
    )
    // console.log('Транзакции загружены из кэша для организации ID:', organization.value.id)
  } else {
    const transactionsResponse = await fetch(`http://localhost:8000/api/transactions?account_id=${orgData.account_id}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })

    if (!transactionsResponse.ok) {
      console.warn('Ошибка при получении транзакций:', transactionsResponse.statusText)
      return
    }

    const transactionsData = await transactionsResponse.json()
    organization.value.incomingTransactions = transactionsData.filter(
      tx => tx.receiver_account_id === orgData.account_id
    )
    organization.value.outgoingTransactions = transactionsData.filter(
      tx => tx.sender_account_id === orgData.account_id
    )

    localStorage.setItem(transactionsKey, JSON.stringify(transactionsData))
    // console.log('Транзакции загружены с сервера и сохранены в кэше для организации ID:', organization.value.id)
  }

  // console.log('Организация получена:', organization.value)
})
</script>

<style scoped>
.text-darkBlue {
  color: #1E3A8A;
}

.donate-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
}

.modal-overlay {
  @apply fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50;
}

.modal-content {
  @apply bg-white rounded-lg shadow-lg w-11/12 sm:w-96 p-6;
}

.predefined-amount-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded;
}

.predefined-amount-button.bg-blue-700 {
  @apply border-2 border-white;
}

.custom-amount-input {
  @apply w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.custom-comment-input {
  @apply w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.error-message {
  @apply text-red-500 text-sm mt-2;
}

.back-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
}

.menu-container {
  @apply flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0;
}

.menu-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
}
</style>
