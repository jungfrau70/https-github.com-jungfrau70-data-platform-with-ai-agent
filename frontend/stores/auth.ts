import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as any,
        accessToken: null as string | null,
        loading: false,
        error: null as string | null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
    },
    actions: {
        async login(email: string, password: string) {
            const config = useRuntimeConfig()
            this.loading = true
            this.error = null
            try {
                const formData = new FormData()
                formData.append('username', email)
                formData.append('password', password)

                const response = await axios.post(`${config.public.apiBase}/auth/login/access-token`, formData)

                this.accessToken = response.data.access_token
                this.user = { email } // Placeholder
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Login failed'
                throw err
            } finally {
                this.loading = false
            }
        },
        async signup(email: string, password: string, nickname: string) {
            const config = useRuntimeConfig()
            this.loading = true
            this.error = null
            try {
                await axios.post(`${config.public.apiBase}/auth/signup`, {
                    email,
                    password,
                    nickname
                })
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Signup failed'
                throw err
            } finally {
                this.loading = false
            }
        },
        logout() {
            this.user = null
            this.accessToken = null
            // Clear cookies if applicable
        }
    }
})
