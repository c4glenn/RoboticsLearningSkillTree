<template>
  <form @submit.prevent="submit">
    <input v-model="username" placeholder="Username" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
    <p v-if="error_string">{{ error_string }}</p>
  </form>
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
