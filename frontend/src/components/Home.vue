<template>
  <div class="flex justify-center items-start gap-15">
    <div class="w-80 p-8 space-y-6 bg-white dark:bg-gray-800 rounded shadow-md">
      <h2 class="text-2xl font-bold text-center dark:text-white text-gray-800">Community</h2>

    </div>
    <div class="w-140 p-8 space-y-6 bg-white dark:bg-gray-800 rounded shadow-md scale-105 text-center">

      <div v-if="!auth.isAuthenticated">
        <h2 class="text-2xl font-bold text-center dark:text-white text-gray-800">Welcome to Robotics Skill Tree</h2>
        <p class="text-center text-gray-600 dark:text-gray-400">
          This is a platform to learn about robotics in a gamified way.
          Explore the skill tree, track your progress and learn robotics.
        </p>
        <RouterLink to="/about">
          <button class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            Learn More
          </button>
        </RouterLink>
        <hr class="my-4 border-gray-300 dark:border-gray-600" />

      </div>

      <h2 class="text-2xl font-bold text-center dark:text-white text-gray-800">Next Up</h2>
      <div v-if="auth.isAuthenticated && auth.user" class="flex flex-col items-center">

      </div>
      <div v-else class="text-center text-gray-500 dark:text-gray-400">
        <p class="mb-4">Please <RouterLink to="/login" class="text-blue-300 hover:underline">Login</RouterLink>/
          <RouterLink to="/register" class="text-blue-300 hover:underline">Register</RouterLink> to see your next steps.
        </p>
      </div>
    </div>
    <div class="w-80 p-8 space-y-6 bg-white dark:bg-gray-800 rounded shadow-md">
      <Progress />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Progress from "./Progress.vue";

const auth = useAuthStore();
const router = useRouter();

function goLogin() {
  router.push("/login");
}
</script>

<style scoped></style>
