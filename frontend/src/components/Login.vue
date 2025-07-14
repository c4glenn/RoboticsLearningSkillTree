<template class="">
  <div class="flex items-center justify-center h-full dark:bg-sky-950 bg-sky-100 ">
    <form
      @submit.prevent="submit"
      class="w-full max-w-sm p-8 space-y-6 dark:bg-gray-600 bg-white rounded shadow-md"  
    >
      <h2 class="text-2xl font-bold text-center dark:text-white text-gray-800">Login</h2>

      <div>
        <label class="block text-sm font-medium dark:text-white text-gray-700">Username</label>
        <input
          v-model="username"
          type="text"
          placeholder="Enter your username"
          required
          class="w-full px-4 py-2 mt-1 border dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium dark:text-white text-gray-700">Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          class="w-full px-4 py-2 mt-1 border dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        type="submit"
        class="w-full px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700 transition"
      >
        Login
      </button>

      <p v-if="error_string" class="text-sm text-red-600 text-center">
        {{ error_string }}
      </p>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

const username = ref("");
const password = ref("");
const error_string = ref<string | null>(null);

async function submit() {
  error_string.value = null;
  try {
    await auth.login(username.value, password.value);
  } catch (error) {
    console.error("Login failed:", error);
    error_string.value = "Invalid username or password";
  }
}
</script>
