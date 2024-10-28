<template>
    <div class="flex items-center justify-center min-h-screen p-4 transition-all duration-300">
        <div class="bg-white p-12 rounded-3xl shadow-lg w-full max-w-lg transform transition-transform hover:scale-105">
            <h2 class="text-3xl font-semibold text-darkBlue mb-6 text-center">Восстановление пароля</h2>
            <form @submit.prevent="handleReset" class="space-y-4">
                <label class="block text-gray-700" for="email">Электронная почта</label>
                <input
                    v-model="email"
                    type="email"
                    id="email"
                    required
                    class="w-full px-3 py-2 border border-muted rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:border-darkBlue hover:border-primary"
                    placeholder="you@example.com"
                />
                <button type="submit" class="w-full bg-primary text-white py-3 rounded-lg transition-all duration-300 transform hover:bg-darkBlue hover:scale-105 active:scale-95">
                    Отправить ссылку для восстановления
                </button>
            </form>
            <div class="text-center mt-4">
                <router-link to="/" class="text-muted hover:text-darkBlue transition-colors duration-200">
                    Вернуться к входу
                </router-link>
            </div>
        </div>
    </div>
</template>
    
<script setup>
// import { ref } from 'vue';
    
// const email = ref('');
    
// const handleReset = () => {
//     console.log('Reset Password for:', email.value);
// };
</script>
    
<style scoped>
</style>