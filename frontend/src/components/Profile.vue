<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api'; // your axios instance

const user = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: ''
});
const errors = ref<Record<string, string>>({});
const successMessage = ref('');

const loadUser = async () => {
  const { data } = await api.get('/accounts/me/'); // Adjust path
  user.value = { ...data};
  console.log('User data loaded:', user.value);
};

const updateProfile = async () => {
  errors.value = {};
  successMessage.value = '';
  try {
    await api.put('/accounts/me/', user.value);
    successMessage.value = 'Profile updated successfully.';
  } catch (error: any) {
    const data = error.response?.data;
    if (data) {
      for (const key in data) {
        errors.value[key] = data[key][0];
      }
    }
  }
};

onMounted(loadUser);
</script>

<template>
  <form @submit.prevent="updateProfile" class="space-y-4 max-w-xl mx-auto p-6 bg-white dark:bg-gray-800 dark:text-white rounded-xl shadow">
    <h2 class="text-xl font-semibold">Update Profile</h2>

    <div>
      <label>Username</label>
      <input v-model="user.username" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
      <p v-if="errors.username" class="text-red-500">{{ errors.username }}</p>
    </div>

    <div>
      <label>Email</label>
      <input v-model="user.email" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
      <p v-if="errors.email" class="text-red-500">{{ errors.email }}</p>
    </div>

    <div>
      <label>First Name</label>
      <input v-model="user.first_name" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
    </div>

    <div>
      <label>Last Name</label>
      <input v-model="user.last_name" class="w-full p-2 rounded border dark:bg-gray-700 dark:text-white" />
    </div>

    <div>
        <p>Reset password: Ability Coming soon</p>
    </div>

    <p v-if="successMessage" class="text-green-500">{{ successMessage }}</p>

    <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 btn-primary">Update Profile</button>
  </form>
</template>