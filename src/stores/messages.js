import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { profilePhotoUrl } from '../services/api'

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
      const raw = response.data
      if (!Array.isArray(raw)) {
        error.value = 'Unexpected response from server'
        conversations.value = []
        return conversations.value
      }
      conversations.value = raw.map(normalizeConversation)
      return conversations.value
    } catch (err) {
      const d = err.response?.data
      error.value = d?.errors?.[0] || d?.error || 'Failed to fetch conversations'
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
      const raw = response.data
      if (!Array.isArray(raw)) {
        error.value = raw?.error || 'Could not load messages'
        currentMessages.value = []
        return currentMessages.value
      }
      currentMessages.value = raw.map(normalizeMessage)
      currentConversation.value = userId
      return currentMessages.value
    } catch (err) {
      const d = err.response?.data
      error.value = d?.errors?.[0] || d?.error || 'Failed to fetch messages'
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
      const d = err.response?.data
      error.value = d?.errors?.[0] || d?.error || 'Failed to send message'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Poll for new messages
  async function pollMessages(userId) {
    try {
      const response = await api.get(`/api/messages/${userId}`)
      const raw = response.data
      if (!Array.isArray(raw)) return
      currentMessages.value = raw.map(normalizeMessage)
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
        photo: profilePhotoUrl(user.profile_photo),
      },
      lastMessage: convo.last_message || '',
      lastMessageAt: convo.last_message_at || null,
      unread: convo.unread || 0,
    }
  }

  function toUserId(v) {
    if (v == null || v === '') return null
    const n = Number(v)
    return Number.isNaN(n) ? null : n
  }

  function normalizeMessage(msg = {}) {
    const senderRaw = msg.sender_id ?? msg.senderId
    const receiverRaw = msg.receiver_id ?? msg.receiverId
    return {
      id: msg.id,
      senderId: toUserId(senderRaw),
      receiverId: toUserId(receiverRaw),
      content: msg.content || '',
      createdAt: msg.created_at ?? msg.createdAt,
      edited: Boolean(msg.edited),
    }
  }

  return {
    conversations, currentMessages, currentConversation, loading, error,
    fetchConversations, fetchMessages, sendMessage, pollMessages, clearMessages
  }
})