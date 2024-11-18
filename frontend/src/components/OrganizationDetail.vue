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
  const { amount, comment } = donationData

  if (!amount || amount < 1) {
    return
  }

  const organizationId = parseInt(route.params.id, 10)

  const newTransaction = {
    sender_account_id: 1,
    receiver_account_id: organizationId,
    amount: amount,
    description: comment || 'Пожертвование без комментария',
    timestamp: new Date().toISOString(),
    transaction_type: 'donation',
  }

  try {
    const response = await fetch(`/api/accounts/${organizationId}/transactions`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTransaction),
    })

    if (!response.ok) {
      return
    }

    const createdTransaction = await response.json()
    newTransaction.id = createdTransaction.id

    if (newTransaction.receiver_account_id === organization.value.account_id) {
      organization.value.incomingTransactions.push(newTransaction)
    }
    if (newTransaction.sender_account_id === organization.value.account_id) {
      organization.value.outgoingTransactions.push(newTransaction)
    }
  } finally {
    closeModal()
  }
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
  const organizationId = parseInt(route.params.id, 10)

  const uniqueTransactions = Array.from(new Set([
    ...organization.value.incomingTransactions,
    ...organization.value.outgoingTransactions,
  ].map(tx => JSON.stringify(tx))))
    .map(tx => JSON.parse(tx))

  return uniqueTransactions.filter(tx =>
    tx.receiver_account_id === organizationId
  ).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})

const fetchOrganizationData = async (id) => {
  isLoading.value = true
  error.value = null

  try {
    const organizationsResponse = await fetch('/api/charity_organizations', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })

    if (!organizationsResponse.ok) {
      throw new Error('Ошибка при получении списка организаций')
    }

    const organizationsData = await organizationsResponse.json()
    const orgData = organizationsData.find(org => org.id === id)

    if (!orgData) {
      throw new Error('Организация с таким ID не найдена.')
    }

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

    const transactionsResponse = await fetch(`/api/accounts/${organization.value.account_id}/transactions`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })

    if (!transactionsResponse.ok) {
      throw new Error('Ошибка при получении транзакций')
    }

    let transactionsData = await transactionsResponse.json()

    transactionsData = transactionsData.filter(
      tx => tx.receiver_account_id === organization.value.account_id || tx.sender_account_id === organization.value.account_id
    )

    organization.value.incomingTransactions = transactionsData.filter(
      tx => tx.receiver_account_id === organization.value.account_id
    )
    organization.value.outgoingTransactions = transactionsData.filter(
      tx => tx.sender_account_id === organization.value.account_id
    )
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
