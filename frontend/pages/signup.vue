<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Create your account
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSignup">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input id="email-address" name="email" type="email" autocomplete="email" required v-model="email" class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm" placeholder="Email address" />
          </div>
           <div>
            <label for="nickname" class="sr-only">Nickname</label>
            <input id="nickname" name="nickname" type="text" required v-model="nickname" class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm" placeholder="Nickname" />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input id="password" name="password" type="password" autocomplete="new-password" required v-model="password" class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm" placeholder="Password" />
          </div>
        </div>

        <div v-if="authStore.error" class="text-red-500 text-sm text-center">
            {{ authStore.error }}
        </div>

        <div>
          <button type="submit" :disabled="authStore.loading" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
            <span v-if="authStore.loading">Creating account...</span>
            <span v-else>Sign up</span>
          </button>
        </div>
      </form>
       <div class="text-center">
        <NuxtLink to="/login" class="font-medium text-primary hover:text-blue-500">
            Already have an account? Sign in
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const email = ref('')
const nickname = ref('')
const password = ref('')
const router = useRouter()

const handleSignup = async () => {
    try {
        await authStore.signup(email.value, password.value, nickname.value)
        alert('Account created! Please sign in.')
        router.push('/login')
    } catch (e) {
        // Error handled in store
    }
}
</script>
