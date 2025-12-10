import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useChatStore = defineStore('chat', {
    state: () => ({
        conversations: [] as any[],
        currentConversationId: null as string | null,
        messages: [] as any[],
        loading: false,
        error: null as string | null,
    }),
    actions: {
        async fetchConversations() {
            const config = useRuntimeConfig()
            const authStore = useAuthStore()
            this.loading = true
            try {
                const response = await axios.get(`${config.public.apiBase}/chat/conversations`, {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` }
                })
                this.conversations = response.data
            } catch (err: any) {
                this.error = err.message
            } finally {
                this.loading = false
            }
        },
        async createConversation(title: string) {
            const config = useRuntimeConfig()
            const authStore = useAuthStore()
            try {
                const response = await axios.post(`${config.public.apiBase}/chat/conversations`,
                    { title },
                    { headers: { Authorization: `Bearer ${authStore.accessToken}` } }
                )
                this.conversations.unshift(response.data)
                this.currentConversationId = response.data.id
                this.messages = [] // New chat has no messages
                return response.data
            } catch (err: any) {
                this.error = err.message
                throw err
            }
        },
        async fetchMessages(conversationId: string) {
            const config = useRuntimeConfig()
            const authStore = useAuthStore()
            this.loading = true
            this.currentConversationId = conversationId
            try {
                const response = await axios.get(`${config.public.apiBase}/chat/conversations/${conversationId}/messages`, {
                    headers: { Authorization: `Bearer ${authStore.accessToken}` }
                })
                this.messages = response.data
            } catch (err: any) {
                this.error = err.message
            } finally {
                this.loading = false
            }
        },
        async sendMessage(content: string) {
            if (!this.currentConversationId) return;

            const config = useRuntimeConfig()
            const authStore = useAuthStore()

            // Optimistic update
            const userMsg = {
                id: 'temp-' + Date.now(),
                role: 'user',
                content,
                timestamp: new Date().toISOString()
            }
            this.messages.push(userMsg)

            try {
                const response = await axios.post(`${config.public.apiBase}/chat/conversations/${this.currentConversationId}/messages`,
                    { role: 'user', content },
                    { headers: { Authorization: `Bearer ${authStore.accessToken}` } }
                )
                // Replace optimistically added message or append response (which is AI response)
                // The API currently returns the AI response. 
                // We should ideally fetch the user message ID back or just trust the optimistic one.
                // Let's push the AI response.
                this.messages.push(response.data)
            } catch (err: any) {
                this.error = err.message
                // TODO: Remove optimistic message on failure
            }
        }
    }
})
