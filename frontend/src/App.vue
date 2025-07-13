<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '@/stores/auth'

const open = ref(false)
const page = ref<HTMLElement | null>(null)
const auth = useAuthStore()

const toggleDropdown = () => {
  open.value = !open.value
  console.log('Dropdown toggled - open:', open.value)

}

const handleOutsideClick = (e: MouseEvent) => {
  if (page.value && !page.value.contains(e.target as Node)) {
    open.value = false
  }
}

// Optional: make sure clicks outside the component close the dropdown
onMounted(() => {
  window.addEventListener('click', handleOutsideClick)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleOutsideClick)
})

</script>

<template>
  <div class="flex flex-col min-h-screen font-sans">
  <header class="bg-gray-800 text-white p-4">
    <div class="container mx-auto flex justify-between items-center">
      <h1 class="text-xl font-bold">Robotics Skill Tree</h1>
      <nav>
        <ul class="flex space-x-4">
          <li>
            <RouterLink to="/" class="hover:underline">Home</RouterLink>
          </li>
          <li>
            <RouterLink to="/skills" class="hover:underline">Skills</RouterLink>
          </li>
          <li>
            <RouterLink to="/about" class="hover:underline">About</RouterLink>
          </li>
          <li>
            <RouterLink to="/contact" class="hover:underline">Contact</RouterLink>
          </li>
          <div v-if="!auth.isAuthenticated">
            <li>
              <RouterLink to="/login" class="hover:underline">Login</RouterLink>
            </li>
            <li>
              <RouterLink to="/register" class="hover:underline">Register</RouterLink>
            </li>
          </div>
          
        </ul>
      </nav>
    </div>
  </header>
  <main class="container mb-auto p-4" ref="page">
    <RouterView />
  </main>
  <footer class="bg-gray-800 text-white p-4 mt-8">
    <div class="container mx-auto text-center">
      <p>&copy; 2023 Tech Mages Lair. All rights reserved.</p>
    </div>
  </footer> 
</div>

</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

pre, code {
  font-family: 'JetBrains Mono', monospace;
}
</style>

