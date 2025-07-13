<template>
  <div class="home">
    <h1>Welcome to Robotics Skill Tree</h1>

    <div v-if="!auth.isAuthenticated">
      <button @click="goLogin">Login</button>
    </div>

    <div v-else>
      <p>Hello, {{ auth.user?.username || 'User' }}!</p>
      <button @click="auth.logout">Logout</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();

function goLogin() {
  router.push("/login");
}
</script>

<style scoped>
.home {
  max-width: 600px;
  margin: 3rem auto;
  text-align: center;
}
button {
  padding: 0.5rem 1.5rem;
  font-size: 1.1rem;
  cursor: pointer;
}
</style>
