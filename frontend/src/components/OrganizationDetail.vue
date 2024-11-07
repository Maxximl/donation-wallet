  <template>
    <div class="flex flex-col h-screen p-4">
      <div class="max-w-3xl mx-auto flex flex-col flex-1">
        <div class="mb-6">
          <h1 class="text-4xl font-semibold text-darkBlue mb-4 text-center">
            {{ organization.name }}
          </h1>
          <p class="text-gray-700 mb-6 text-center">
            {{ organization.description }}
          </p>
        </div>

        <h2 class="text-2xl font-semibold text-darkBlue mb-4 text-center">
          Транзакции:
        </h2>
        <div class="flex-1 mb-6 flex flex-col">
          <div
            v-if="mergedTransactions.length > 0"
            :class="['space-y-4', mergedTransactions.length > 4 ? 'overflow-y-auto' : '']"
            :style="mergedTransactions.length > 4 ? 'max-height: calc(100vh - 300px)' : 'max-height: none'"
          >
            <div
              v-for="transaction in mergedTransactions"
              :key="`${transaction.type}-${transaction.timestamp}`"
              class="transaction-card"
            >
              <div class="flex-1">
                <p class="text-gray-600">{{ formatDate(transaction.timestamp) }}</p>
                <p class="font-medium">{{ transaction.description }}</p>
              </div>
              <div class="flex items-center mt-2 sm:mt-0">
                <span
  :class="{
    'text-green-600': transaction.transaction_type === 'donation',
    'text-red-600': transaction.transaction_type === 'deposit',
  }"
  class="transaction-amount mr-4"
>
  {{ transaction.transaction_type === 'donation' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
</span>


                <span class="text-sm text-gray-500">{{ transaction.comment }}</span>
              </div>
            </div>
          </div>

          <div v-else class="text-center text-gray-500">
            Нет транзакций для отображения.
          </div>
        </div>

        <div
          class="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0"
        >
        <button @click="goBack" class="back-button w-full sm:w-auto">
            Назад
          </button>

          <button @click="openModal" class="donate-button w-full sm:w-auto">
            Отправить пожертвование
          </button>
        </div>
      </div>
  
      <div v-if="isModalOpen" class="modal-overlay">
        <div class="modal-content">
          <h3 class="text-xl font-semibold mb-4">Выберите сумму пожертвования</h3>
          <div class="space-y-4">
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="amount in predefinedAmounts" 
                :key="amount" 
                @click="selectAmount(amount)"
                :class="['predefined-amount-button', selectedAmount === amount ? 'bg-blue-700' : '']"
              >
                {{ formatCurrency(amount) }}
              </button>
            </div>
            
            <div v-if="selectedAmount" class="mt-4 text-center">
              Вы выбрали: <strong>{{ formatCurrency(selectedAmount) }}</strong>
            </div>
            
            <div>
              <label for="customAmount" class="block text-gray-700 mb-2">Или введите свою сумму:</label>
              <input 
                type="number" 
                id="customAmount" 
                v-model.number="customAmount" 
                min="1" 
                placeholder="Введите сумму"
                class="custom-amount-input"
              >
            </div>
            <div>
              <label for="customAmount" class="block text-gray-700 mb-2">Введите комментарий к платежу:</label>
            <textarea 
                type="string" 
                id="Comment" 
                v-model.number="Comment" 
                placeholder="Введите комментарий"
                class="custom-comment-input"
              >
            </textarea>
            </div>
          </div>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          
          <div class="action-buttons">
            <button @click="closeModal" class="cancel-button">
              Отмена
            </button>
            <button @click="submitDonation" class="submit-button">
              Пожертвовать
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'

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
    incomingTransactions: [],
    outgoingTransactions: [],
  })

  const isModalOpen = ref(false)
  const predefinedAmounts = [500, 1000, 2000, 5000]
  const customAmount = ref(null)
  const selectedAmount = ref(null)
  const errorMessage = ref('')

  const openModal = () => {
    isModalOpen.value = true
    selectedAmount.value = null
    customAmount.value = null
    errorMessage.value = ''
  }

  const closeModal = () => {
    isModalOpen.value = false
  }

  const selectAmount = (amount) => {
    selectedAmount.value = amount
    customAmount.value = null
    errorMessage.value = ''
  }

  const submitDonation = async () => {
    let amount = selectedAmount.value || customAmount.value

    if (!amount || amount < 1) {
      errorMessage.value = 'Пожалуйста, выберите или введите корректную сумму.'
      return
    }

    const newTransaction = {
      sender_account_id: organization.value.id,
      receiver_account_id: organization.value.id, // what? id?
      amount: amount,
      description: 'Пожертвование через интерфейс',
      timestamp: new Date().toISOString(),
      transaction_type: 'donation',
    }

    const response = await fetch('http://localhost:8000/api/transactions', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTransaction),
    })

    if (!response.ok) {
      errorMessage.value = 'Ошибка при создании транзакции: ' + response.statusText
      return
    }

    const createdTransaction = await response.json()
    organization.value.incomingTransactions.push({
      ...newTransaction,
      id: createdTransaction.id,
    })
    
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
      incomingTransactions: [],
      outgoingTransactions: [],
    }

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
    organization.value.incomingTransactions = transactionsData.filter(tx => tx.receiver_account_id === orgData.account_id)
    organization.value.outgoingTransactions = transactionsData.filter(tx => tx.sender_account_id === orgData.account_id)

    console.log('Организация получена:', organization.value)
  })
  </script>

  <style scoped>
  .text-darkBlue {
    color: #1E3A8A;
  }

  .transaction-card {
    @apply flex flex-col sm:flex-row justify-between items-start sm:items-center p-4 bg-white shadow rounded-lg;
  }

  .transaction-amount {
    @apply font-semibold mr-4;
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

  .custom-comment-input{
    @apply w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500;
  }

  .error-message {
    @apply text-red-500 text-sm mt-2;
  }

  .action-buttons {
    @apply flex justify-end mt-6 space-x-2;
  }

  .cancel-button {
    @apply bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded;
  }

  .submit-button {
    @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded;
  }

  .back-button {
    @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full sm:w-auto;
  }

  @media (min-width: 640px) {
    .transaction-card {
      @apply flex-row;
    }
  }
  </style>
