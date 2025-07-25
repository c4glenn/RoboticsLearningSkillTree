<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { SunIcon, MoonIcon } from '@heroicons/vue/24/solid';

const auth = useAuthStore();
const isOpen = ref(false);
const isDark = ref(false);
const router = useRouter();

function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

function logout() {
  auth.logout(); // Or whatever your logout method is
  isOpen.value = false;
}

function toggleDarkMode() {
  isDark.value = !isDark.value;
  document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
}
onMounted(() => {
  isDark.value = localStorage.getItem("theme") === "dark";
  if (localStorage.getItem("theme") === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  if (auth.isAuthenticated) {
    try {
      // Fetch user profile on mount
      auth.fetchUserProfile();
    } catch (error) {
      console.error("Failed to fetch user profile:", error);
    }
  }
});


// Optional: basic click outside directive
function handleClickOutside(event: MouseEvent) {
  if (!(event.target as HTMLElement).closest(".relative")) {
    isOpen.value = false;
  }
}


onMounted(() => document.addEventListener("click", handleClickOutside));
onBeforeUnmount(() => document.removeEventListener("click", handleClickOutside));
</script>

<template>
  <div class="flex flex-col min-h-screen font-sans">
    <header class="dark:bg-gray-600 bg-gray-300 dark:text-white p-4">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold">
          <RouterLink to="/" class="hover:underline">Robotics Skill Tree</RouterLink>
        </h1>
        <nav>
          <ul class="flex space-x-4">
            <li>
              <button @click="toggleDarkMode" class="p-2 transition-transform duration-300 hover:rotate-12">
                <Transition name="fade" mode="out-in">
                  <component :is="isDark ? MoonIcon : SunIcon" class="h-6 w-6 text-yellow-400 dark:text-gray-200"
                    key="theme-icon" />
                </Transition>
              </button>
            </li>

            <li>
              <RouterLink to="/skills" class="hover:underline">Full Skill Tree</RouterLink>
            </li>
            <li>
              <RouterLink to="/about" class="hover:underline">About</RouterLink>
            </li>
            <template v-if="!auth.user">
              <li>
                <RouterLink to="/login" class="hover:underline">Login</RouterLink>
              </li>
              <li>
                <RouterLink to="/register" class="hover:underline">Register</RouterLink>
              </li>
            </template>
            <template v-else>
              <li class="relative flex items-center">
                <button @click="toggleDropdown" class="flex items-center gap-1 text-sm font-medium hover:underline">
                  {{ auth.user?.username || "User" }}
                  <svg class="w-3 h-3" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="2" />
                  </svg>
                </button>

                <div v-if="isOpen" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-md shadow-lg z-50">
                  <ul>
                    <li>
                      <RouterLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        User Profile
                      </RouterLink>
                    </li>
                    <li>
                      <RouterLink to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        Settings
                      </RouterLink>
                    </li>
                    <li>
                      <button @click="logout" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                        Sign out
                      </button>
                    </li>
                  </ul>
                </div>
              </li>
            </template>

          </ul>
        </nav>
      </div>
    </header>
    <main class="w-full p-4 dark:bg-sky-950 bg-sky-100 flex-grow" ref="page">
      <RouterView />
    </main>
    <footer class="dark:bg-gray-600 bg-gray-300 dark:text-white p-4">
      <div class="container mx-auto text-center">
        <p>&copy; 2023 Tech Mages Lair. All rights reserved.</p>
      </div>
    </footer>
  </div>

</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.font-sans {
  font-family: 'Inter', sans-serif;
}

code {
  font-family: 'JetBrains Mono', monospace;
}
</style>
