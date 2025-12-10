import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useAnalysisStore = defineStore('analysis', {
    state: () => ({
        summary: null as any,
        loading: false,
        error: null as string | null,
    }),
    actions: {
        async uploadFile(file: File) {
            const config = useRuntimeConfig()
            const authStore = useAuthStore()
            this.loading = true
            this.error = null

            const formData = new FormData()
            formData.append('file', file)

            try {
                const response = await axios.post(`${config.public.apiBase}/analysis/upload`, formData, {
                    headers: {
                        Authorization: `Bearer ${authStore.accessToken}`,
                        'Content-Type': 'multipart/form-data'
                    }
                })
                this.summary = response.data
            } catch (err: any) {
                this.error = err.response?.data?.detail || err.message
            } finally {
                this.loading = false
            }
        }
    }
})
