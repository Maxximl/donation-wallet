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
            :key="`${transaction.type}-${transaction.id}`"
            class="transaction-card"
          >
            <div class="flex-1">
              <p class="text-gray-600">{{ formatDate(transaction.date) }}</p>
              <p class="font-medium">{{ transaction.description }}</p>
            </div>
            <div class="flex items-center mt-2 sm:mt-0">
              <span
                :class="{
                  'text-green-600': transaction.type === 'incoming',
                  'text-red-600': transaction.type === 'outgoing',
                }"
                class="transaction-amount mr-4"
              >
                {{ transaction.type === 'incoming' ? '+' : '-' }}{{
                  formatCurrency(transaction.amount)
                }}
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
        <button @click="openModal" class="donate-button w-full sm:w-auto">
          Отправить пожертвование
        </button>

        <button @click="goBack" class="back-button w-full sm:w-auto">
          Назад
        </button>
      </div>
    </div>

    <!-- Модальное окно -->
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
  image: '',
  fundingGoal: 0,
  currentFunding: 0,
  author: '',
  date: '',
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
  console.log('Выбрано:', amount)
}

const submitDonation = () => {
  let amount = selectedAmount.value || customAmount.value

  if (!amount || amount < 1) {
    errorMessage.value = 'Пожалуйста, выберите или введите корректную сумму.'
    return
  }

  console.log('Пожертвование:', amount)

  const newTransaction = {
    id: Date.now(),
    date: new Date().toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }),
    amount: amount,
    source: 'Пожертвование пользователя',
    comment: 'Пожертвование через интерфейс',
  }

  organization.value.incomingTransactions.push(newTransaction)
  organization.value.currentFunding += amount
  closeModal()
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [day, month, year] = dateStr.split('.')
  const date = new Date(`${year}-${month}-${day}`)
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
  if (!organization.value.id) return []

  const incoming = organization.value.incomingTransactions.map(tx => ({
    ...tx,
    type: 'incoming',
    description: tx.source,
  }))
  
  const outgoing = organization.value.outgoingTransactions.map(tx => ({
    ...tx,
    type: 'outgoing',
    description: tx.purpose,
  }))
  
  return [...incoming, ...outgoing].sort((a, b) => {
    const dateA = new Date(a.date.split('.').reverse().join('-'))
    const dateB = new Date(b.date.split('.').reverse().join('-'))
    return dateB - dateA
  })
})

onMounted(() => {
  const id = parseInt(route.params.id, 10)
  console.log('Полученный ID организации:', id)

  const organizations = [
    {
      id: 1,
      name: 'Помощь детям',
      description: 'Организация, предоставляющая поддержку детям из неблагополучных семей.',
      image: 'https://via.placeholder.com/400x200.png?text=Помощь+детям',
      fundingGoal: 50000,
      currentFunding: 15000,
      author: 'Иван Иванов',
      date: '01.04.2024',
      incomingTransactions: [
        { id: 1, date: '05.04.2024', amount: 5000, source: 'Частный донор', comment: 'Пожертвование' },
        { id: 2, date: '10.04.2024', amount: 10000, source: 'Корпоративный спонсор', comment: 'Спонсорская поддержка' },
      ],
      outgoingTransactions: [
        { id: 1, date: '15.04.2024', amount: 3000, purpose: 'Покупка игрушек', comment: 'Закупка для детей' },
        { id: 2, date: '20.04.2024', amount: 2000, purpose: 'Организация мероприятий', comment: 'Проведение праздника' },
      ],
    },
    {
      id: 2,
      name: 'Здоровье для всех',
      description: 'Благотворительная организация, занимающаяся медицинской помощью нуждающимся.',
      image: 'https://via.placeholder.com/400x200.png?text=Здоровье+для+всех',
      fundingGoal: 75000,
      currentFunding: 30000,
      author: 'Мария Петрова',
      date: '15.04.2024',
      incomingTransactions: [
        { id: 3, date: '18.04.2024', amount: 15000, source: 'Благотворительный фонд', comment: 'Грант' },
      ],
      outgoingTransactions: [
        { id: 3, date: '22.04.2024', amount: 5000, purpose: 'Медицинское оборудование', comment: 'Закупка аппаратов' },
      ],
    },
    {
      id: 3,
      name: 'Экология Земли',
      description: 'Организация, работающая над сохранением окружающей среды и природных ресурсов.',
      image: 'https://via.placeholder.com/400x200.png?text=Экология+Земли',
      fundingGoal: 60000,
      currentFunding: 45000,
      author: 'Алексей Смирнов',
      date: '20.04.2024',
      incomingTransactions: [
        { id: 4, date: '25.04.2024', amount: 20000, source: 'Государственный грант', comment: 'Поддержка проекта' },
      ],
      outgoingTransactions: [
        { id: 4, date: '28.04.2024', amount: 10000, purpose: 'Покупка оборудования', comment: 'Оборудование для очистки' },
      ],
    },
  ]

  const foundOrganization = organizations.find(o => o.id === id)

  if (foundOrganization) {
    organization.value = foundOrganization
    console.log('Организация найдена:', organization.value)
  } else {
    organization.value = {
      id: null,
      name: '',
      description: '',
      image: '',
      fundingGoal: 0,
      currentFunding: 0,
      author: '',
      date: '',
      incomingTransactions: [],
      outgoingTransactions: [],
    }
    console.warn('Организация с таким ID не найдена.')
  }
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
