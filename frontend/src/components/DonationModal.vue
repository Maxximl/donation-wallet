<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="text-xl font-semibold mb-4">Выберите сумму пожертвования</h3>
      <div class="space-y-4">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="amount in predefinedAmounts"
            :key="amount"
            @click="selectAmount(amount)"
            :class="['predefined-amount-button', selectedAmount === amount ? 'bg-blue-700' : '']"
            :disabled="isSubmitting"
          >
            {{ formatCurrency(amount) }}
          </button>
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
            :disabled="isSubmitting"
          >
        </div>

        <div>
          <label for="comment" class="block text-gray-700 mb-2">Введите комментарий к платежу:</label>
          <textarea
            id="comment"
            v-model="comment"
            placeholder="Введите комментарий"
            class="custom-comment-input"
            :disabled="isSubmitting"
          ></textarea>
        </div>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div class="action-buttons">
        <button @click="$emit('close-modal')" class="cancel-button" :disabled="isSubmitting">
          Отмена
        </button>
        <button @click="handleSubmitDonation" class="submit-button" :disabled="isSubmitting">
          {{ isSubmitting ? 'Отправка...' : 'Пожертвовать' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  isModalOpen: {
    type: Boolean,
    required: true,
  },
  predefinedAmounts: {
    type: Array as () => number[],
    default: () => [],
  },
  formatCurrency: {
    type: Function,
    required: true,
  },
  isSubmitting: { 
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['close-modal', 'submit-donation']);

const selectedAmount = ref<number | null>(null);
const customAmount = ref<number | null>(null);
const comment = ref('');
const errorMessage = ref('');

watch(selectedAmount, (newAmount) => {
  customAmount.value = newAmount;
});

const selectAmount = async (amount: number) => {
  if (props.isSubmitting) return; 
  selectedAmount.value = amount;
  customAmount.value = amount;
  errorMessage.value = '';

  await nextTick();
  // alert(`Вы выбрали: ${props.formatCurrency(amount)}`);
};

const handleSubmitDonation = () => {
  let amount = selectedAmount.value || customAmount.value;

  if (!amount || amount < 1) {
    errorMessage.value = 'Пожалуйста, выберите или введите корректную сумму.';
    return;
  }

  emit('submit-donation', { amount: amount, comment: comment.value });
};
</script>

<style scoped>
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

.action-buttons {
  @apply flex justify-end mt-6 space-x-2;
}

.cancel-button {
  @apply bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded;
}

.submit-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded;
}

button:disabled,
button[disabled] {
  @apply opacity-50 cursor-not-allowed;
}
</style>
