<template>
  <div class="container">
    <div class="card"> 
      <h2 class="title">{{ isReset ? 'Восстановление пароля' : 'Вход в систему' }}</h2>
      <form @submit.prevent="isReset ? handleReset : handleLogin" class="space-y-4">
        <label class="label" for="email">Электронная почта</label>
        <input
          v-model="email"
          type="email"
          id="email"
          required
          class="input"
          placeholder="you@example.com"
        />
        <div v-if="!isReset">
          <label class="label" for="password">Пароль</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="input"
            placeholder="••••••••"
          />
        </div>
        <div v-else class="invisible">
          <label class="label" for="password">Пароль</label>
          <input
            type="password"
            id="password"
            class="input"
            placeholder=""
            disabled
          />
        </div>
        <button type="submit" class="button" @click="isReset ? handleReset() : handleLogin()">
          {{ isReset ? 'Отправить ссылку для восстановления' : 'Войти' }}
        </button>
      </form>
      <div class="footer">
        <a @click.prevent="toggleForm" class="link">
          {{ isReset ? 'Вернуться к входу' : 'Забыли пароль?' }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const defaultEmail = 'user@example.com';
const defaultPassword = 'password123';

const email = ref(defaultEmail);
const password = ref(defaultPassword);
const isReset = ref(false);

const router = useRouter();

const handleLogin = () => {
  if (email.value === defaultEmail && password.value === defaultPassword) {
    router.push('/posts');
  } else {
    alert('Неверный логин или пароль');
  }
};

const handleReset = () => {
  console.log('Reset Password for:', email.value);
};

const toggleForm = () => {
  isReset.value = !isReset.value;
  email.value = '';
  password.value = '';
};
</script>

<style scoped>
.container {
  @apply flex min-h-screen items-center justify-center p-4;
}

.card {
  @apply bg-white p-12 rounded-3xl shadow-lg w-96;
}

.title {
  @apply text-4xl font-semibold text-darkBlue mb-10 text-center;
}

.label {
  @apply block text-gray-700 mb-2;
}

.input {
  @apply w-full px-4 py-3 mb-6 border border-muted rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-darkBlue;
}

.button {
  @apply w-full bg-primary text-white py-3 px-4 rounded-lg;
}

.footer {
  @apply text-center mt-6;
}

.link {
  @apply text-muted cursor-pointer;
}

.invisible {
  visibility: hidden;
}
</style>
