<template>
  <div class="min-h-screen bg-gray-100 font-sans">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <NuxtLink to="/" class="text-2xl font-bold text-primary">Speckit</NuxtLink>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink to="/" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Home
              </NuxtLink>
              <NuxtLink v-if="authStore.isAuthenticated" to="/chat" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Chat
              </NuxtLink>
              <NuxtLink v-if="authStore.isAuthenticated" to="/dashboard" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Dashboard
              </NuxtLink>
            </div>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:items-center">
             <template v-if="!authStore.isAuthenticated">
                <NuxtLink to="/login" class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium">Log in</NuxtLink>
                <NuxtLink to="/signup" class="bg-primary text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium ml-3">Sign up</NuxtLink>
             </template>
             <template v-else>
                 <span class="text-gray-700 text-sm mr-4">{{ authStore.user?.email }}</span>
                 <button @click="logout" class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                    Log out
                 </button>
             </template>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <slot />
      </div>
    </main>
    
    <footer class="bg-white border-t border-gray-200 mt-auto">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <p class="text-center text-gray-500 text-sm">
                &copy; {{ new Date().getFullYear() }} Speckit (GoldenCircle). All rights reserved.
            </p>
        </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
    authStore.logout()
    router.push('/login')
}
</script>
