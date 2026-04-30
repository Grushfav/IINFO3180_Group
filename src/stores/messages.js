import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { buildMediaUrl } from '../services/api'

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
      conversations.value = response.data.map(normalizeConversation)
      return conversations.value
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
      currentMessages.value = response.data.map(normalizeMessage)
      currentConversation.value = userId
      return currentMessages.value
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
      const normalized = normalizeMessage(response.data)
      currentMessages.value.push(normalized)
      return normalized
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
      currentMessages.value = response.data.map(normalizeMessage)
      return currentMessages.value
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

  function normalizeConversation(convo = {}) {
    const user = convo.user || {}
    return {
      id: convo.id,
      user: {
        id: user.user_id || user.id,
        firstName: user.first_name || '',
        lastName: user.last_name || '',
        photo: user.profile_photo ? buildMediaUrl(`/static/uploads/${user.profile_photo}`) : null,
      },
      lastMessage: convo.last_message || '',
      lastMessageAt: convo.last_message_at || null,
      unread: convo.unread || 0,
    }
  }

  function normalizeMessage(msg = {}) {
    return {
      id: msg.id,
      senderId: msg.sender_id,
      receiverId: msg.receiver_id,
      content: msg.content || '',
      createdAt: msg.created_at,
      edited: Boolean(msg.edited),
    }
  }

  return {
    conversations, currentMessages, currentConversation, loading, error,
    fetchConversations, fetchMessages, sendMessage, pollMessages, clearMessages
  }
})