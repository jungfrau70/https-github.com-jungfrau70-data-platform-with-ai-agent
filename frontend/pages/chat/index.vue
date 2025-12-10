<template>
  <div class="flex h-[calc(100vh-64px)]">
    <!-- Sidebar -->
    <div class="w-64 bg-white border-r border-gray-200 overflow-y-auto hidden md:block">
      <div class="p-4 border-b border-gray-200">
        <button @click="createNewChat" class="w-full bg-primary hover:bg-blue-700 text-white font-bold py-2 px-4 rounded font-medium text-sm">
          + New Chat
        </button>
      </div>
      <ul>
        <li v-for="chat in chatStore.conversations" :key="chat.id" :class="{'bg-blue-50': chat.id === chatStore.currentConversationId}" class="hover:bg-gray-50">
          <button @click="selectChat(chat.id)" class="w-full text-left px-4 py-3 text-sm text-gray-700 truncate">
            {{ chat.title }}
          </button>
        </li>
      </ul>
    </div>

    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col bg-gray-50">
      <!-- Messages -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4">
        <div v-if="!chatStore.currentConversationId" class="h-full flex items-center justify-center text-gray-500">
            Select a conversation or start a new one.
        </div>
        <div v-else v-for="msg in chatStore.messages" :key="msg.id" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div class="max-w-[75%] rounded-lg px-4 py-2 text-sm shadow-sm"
               :class="msg.role === 'user' ? 'bg-primary text-white' : 'bg-white text-gray-800 border border-gray-200'">
             <div class="font-bold mb-1 text-xs opacity-75">{{ msg.role === 'user' ? 'You' : 'Gem' }}</div>
             <div class="whitespace-pre-wrap">{{ msg.content }}</div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="bg-white border-t border-gray-200 p-4">
        <form @submit.prevent="handleSend" class="max-w-4xl mx-auto relative flex items-center">
            <input 
                v-model="inputContent" 
                type="text" 
                placeholder="Ask Gem about your data..." 
                class="shadow-sm focus:ring-primary focus:border-primary block w-full pr-12 sm:text-sm border-gray-300 rounded-md py-3 px-4"
                :disabled="!chatStore.currentConversationId || chatStore.loading"
            />
            <button type="submit" :disabled="!inputContent.trim() || chatStore.loading" class="absolute right-2 p-1 text-gray-400 hover:text-primary">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
            </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useChatStore } from '~/stores/chat'

definePageMeta({
  middleware: ["auth"] // Protect this route
})

const chatStore = useChatStore()
const inputContent = ref('')

onMounted(() => {
    chatStore.fetchConversations()
})

const createNewChat = async () => {
    await chatStore.createConversation("New Conversation")
}

const selectChat = async (id) => {
    await chatStore.fetchMessages(id)
}

const handleSend = async () => {
    if (!inputContent.value.trim()) return
    const content = inputContent.value
    inputContent.value = '' // Clear immediately
    await chatStore.sendMessage(content)
}
</script>
