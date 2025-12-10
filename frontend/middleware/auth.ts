
import { useAuthStore } from '~/stores/auth'
import type { RouteLocationNormalized } from 'vue-router'

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized, from: RouteLocationNormalized) => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated && to.path !== '/login' && to.path !== '/signup') {
        return navigateTo('/login')
    }
})
