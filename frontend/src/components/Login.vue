<template>
  <div class="container">
    <div class="card">
      <h2 class="title">Вход в систему</h2>
      <form @submit.prevent="handleLogin">
        <label class="label" for="email">Электронная почта</label>
        <input
          v-model="email"
          type="email"
          id="email"
          required
          class="input"
          placeholder="you@example.com"
        />

        <label class="label" for="password">Пароль</label>
        <input
          v-model="password"
          type="password"
          id="password"
          required
          class="input"
          placeholder="••••••••"
        />

        <button type="submit" class="button">
          Войти
        </button>
      </form>
      <div class="footer">
        <router-link to="/reset-password" class="link">
          Забыли пароль?
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// import { ref } from 'vue';
// import { useRouter } from 'vue-router';

// const email = ref('');
// const password = ref('');
// const router = useRouter();

// const handleLogin = () => {
//   console.log('Email:', email.value);
//   console.log('Password:', password.value);
//   router.push('/posts');
// };
</script>

<style scoped>
.container {
  @apply flex min-h-screen items-center justify-center p-4 transition-all duration-300;
}

.card {
  @apply bg-white p-12 rounded-3xl shadow-lg w-full max-w-lg transform transition-transform hover:scale-105;
}

.title {
  @apply text-4xl font-semibold text-darkBlue mb-10 text-center;
}

.label {
  @apply block text-gray-700 mb-2;
}

.input {
  @apply w-full px-4 py-3 mb-6 border border-muted rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-darkBlue hover:border-primary;
}

.button {
  @apply w-full bg-primary text-white py-3 px-4 rounded-lg transition-all duration-300 transform hover:bg-darkBlue hover:scale-105 active:scale-95;
}

.footer {
  @apply text-center mt-6;
}

.link {
  @apply text-muted hover:text-darkBlue transition-colors duration-200;
}
</style>