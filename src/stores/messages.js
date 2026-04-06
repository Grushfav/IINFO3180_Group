import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useMessagesStore = defineStore('messages', () => {
  // State
  const conversations = ref([])
  const currentMessages = ref([])
  const currentConversation = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Get all conversations for current user
  async function fetchConversations() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/messages')
      conversations.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch conversations'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Get messages between current user and another user
  async function fetchMessages(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/messages/${userId}`)
      currentMessages.value = response.data
      currentConversation.value = userId
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch messages'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Send a message to another user
  async function sendMessage(userId, content) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/messages/${userId}`, { content })
      currentMessages.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to send message'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Edit a message
  async function editMessage(messageId, content) {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/messages/${messageId}`, { content })
      // update message in currentMessages
      const index = currentMessages.value.findIndex(m => m.id === messageId)
      if (index !== -1) {
        currentMessages.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to edit message'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Delete a message
  async function deleteMessage(messageId) {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/messages/${messageId}`)
      // remove message from currentMessages
      currentMessages.value = currentMessages.value.filter(
        m => m.id !== messageId
      )
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete message'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Poll for new messages (near real time)
  async function pollMessages(userId) {
    try {
      const response = await api.get(`/messages/${userId}`)
      currentMessages.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to poll messages'
    }
  }

  // Clear messages
  function clearMessages() {
    conversations.value = []
    currentMessages.value = []
    currentConversation.value = null
    error.value = null
  }

  return {
    conversations,
    currentMessages,
    currentConversation,
    loading,
    error,
    fetchConversations,
    fetchMessages,
    sendMessage,
    editMessage,
    deleteMessage,
    pollMessages,
    clearMessages
  }
})