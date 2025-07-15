<template>
  <div class="flex items-center justify-center h-full bg-sky-100 dark:bg-sky-950">
    <form
      @submit.prevent="submit"
      class="w-full max-w-sm p-8 space-y-6 bg-white dark:bg-gray-800 rounded shadow-md"
    >
      <h2 class="text-2xl font-bold text-center text-gray-800 dark:text-white">Register</h2>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Username</label>
        <input
          v-model="username"
          type="text"
          placeholder="Choose a username"
          required
          class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
        <p v-if="errors.username" class="text-red-500">{{ errors.username }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Email</label>
        <input
          v-model="email"
          type="email"
          placeholder="you@example.com"
          required
          class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
        <p v-if="errors.email" class="text-red-500">{{ errors.email }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">First Name</label>
        <input
          v-model="firstName"
          type="text"
          placeholder="Enter your first name"
          required
          class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Last Name</label>
        <input
          v-model="lastName"
          type="text"
          placeholder="Enter your last name"
          required
          class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
      </div>



      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
        <p v-if="errors.password" class="text-red-500">{{ errors.password }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Confirm Password</label>
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="••••••••"
          required
          class="w-full px-4 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600"
        />
      </div>

      <button
        type="submit"
        class="w-full px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700 transition"
      >
        Register
      </button>

      <p v-if="errors.nonField" class="text-sm text-red-600 text-center">
        {{ errors.nonField }}
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { register } from "@/api";

const auth = useAuthStore();
const router = useRouter();

const username = ref("");
const email = ref("");
const firstName = ref("");
const lastName = ref("");
const password = ref("");
const confirmPassword = ref("");
const errors = ref<{ username?: string; email?: string; password?: string; nonField?: string }>({});

const registerUser = async () => {
  errors.value = {}; // clear previous errors

  try {
    await register(
      username.value,
      email.value,
      password.value,
      firstName.value,
      lastName.value
    );
    auth.login(username.value, password.value); // Automatically log in after registration
    router.push("/home"); // Redirect to home page after successful registration

    // ✅ Registration successful — redirect or notify user
  } catch (error: any) {
    const data = error?.response?.data;

    if (data) {
      errors.value.username = data.username?.[0];
      errors.value.email = data.email?.[0];
      errors.value.password = data.password?.[0];
      errors.value.nonField = data.non_field_errors?.[0];
    } else {
      errors.value.nonField = 'Server or network error.';
    }
  }
};


async function submit() {
  if (password.value !== confirmPassword.value) {
    errors.value.password = "Passwords do not match.";
    return;
  }
  await registerUser();
}
</script>
