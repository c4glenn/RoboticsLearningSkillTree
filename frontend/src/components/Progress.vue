<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore();


</script>

<template>
    <h2 class="text-2xl font-bold text-center dark:text-white text-gray-800">Progress</h2>
    <div v-if="auth.isAuthenticated && auth.user">

    </div>
    <div v-else class="text-center text-gray-500 dark:text-gray-400">
        <p class="mb-4">Please <RouterLink to="/login" class="text-blue-300 hover:underline">Login</RouterLink>/<RouterLink to="/register" class="text-blue-300 hover:underline">Register</RouterLink> to save your progress.</p>
    </div>
</template>