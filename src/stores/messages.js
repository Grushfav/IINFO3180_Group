import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useMessagesStore = defineStore('messages', () => {
  const conversations = ref([])
  const currentMessages = ref([])
  const currentConversation = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // GET /api/messages
  async function fetchConversations() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/messages')
      conversations.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to fetch conversations'
      throw err
    } finally {
      loading.value = false
    }
  }

  // GET /api/messages/<user_id>
  async function fetchMessages(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/messages/${userId}`)
      currentMessages.value = response.data
      currentConversation.value = userId
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to fetch messages'
      throw err
    } finally {
      loading.value = false
    }
  }

  // POST /api/messages/<user_id>
  async function sendMessage(userId, content) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/api/messages/${userId}`, { content })
      currentMessages.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to send message'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Poll for new messages
  async function pollMessages(userId) {
    try {
      const response = await api.get(`/api/messages/${userId}`)
      currentMessages.value = response.data
      return response.data
    } catch (err) {
      // Silent fail for polling
    }
  }

  function clearMessages() {
    conversations.value = []
    currentMessages.value = []
    currentConversation.value = null
    error.value = null
  }

  return {
    conversations, currentMessages, currentConversation, loading, error,
    fetchConversations, fetchMessages, sendMessage, pollMessages, clearMessages
  }
})