<template>
  <div class="messages-page">
    <div class="messages-layout">
      <!-- Sidebar: conversation list -->
      <aside class="convo-sidebar" :class="{ hidden: activeConvo && isMobile }">
        <div class="sidebar-header">
          <h2 class="sidebar-title">Messages</h2>
        </div>

        <div v-if="pageError" class="convo-error">{{ pageError }}</div>

        <div v-if="loadingConvos" class="loading-mini">
          <div class="spinner-sm"></div>
        </div>

        <div v-else-if="conversations.length === 0" class="no-convos">
          <p>No conversations yet.<br/>Match with someone to start chatting!</p>
        </div>

        <ul v-else class="convo-list">
          <li
            v-for="convo in conversations"
            :key="convo.id"
            class="convo-item"
            :class="{ active: activeConvo?.id === convo.id }"
            @click="openConversation(convo)"
          >
            <img :src="convo.user.photo" :alt="convo.user.firstName" class="convo-avatar" />
            <div class="convo-info">
              <div class="convo-name">{{ convo.user.firstName }} {{ convo.user.lastName }}</div>
              <div class="convo-last">{{ convo.lastMessage }}</div>
            </div>
            <div class="convo-right">
              <span class="convo-time">{{ formatTime(convo.lastMessageAt) }}</span>
              <span v-if="convo.unread" class="unread-badge">{{ convo.unread }}</span>
            </div>
          </li>
        </ul>
      </aside>

      <!-- Chat panel -->
      <main class="chat-panel" :class="{ hidden: !activeConvo && isMobile }">
        <div v-if="!activeConvo" class="chat-empty">
          <span>💬</span>
          <p>Select a conversation to start chatting</p>
        </div>

        <template v-else>
          <div class="chat-header">
            <button v-if="isMobile" class="back-btn" @click="activeConvo = null">← Back</button>
            <img :src="activeConvo.user.photo" :alt="activeConvo.user.firstName" class="chat-avatar" />
            <span class="chat-name">{{ activeConvo.user.firstName }} {{ activeConvo.user.lastName }}</span>
          </div>

          <div class="chat-messages" ref="messagesEl">
            <div v-if="loadingMessages" class="loading-mini center">
              <div class="spinner-sm"></div>
            </div>

            <div
              v-for="msg in currentMessages"
              :key="msg.id"
              class="msg-row"
              :class="{ mine: isMine(msg) }"
            >
              <span class="msg-sender-tag">{{ isMine(msg) ? 'You' : (activeConvo.user.firstName || 'Them') }}</span>
              <div class="msg-bubble">
                {{ msg.content }}
                <span v-if="msg.edited" class="msg-edited">(edited)</span>
              </div>
              <div class="msg-time">{{ formatTime(msg.createdAt) }}</div>
            </div>
          </div>

          <div class="chat-input-row">
            <input
              v-model="newMessage"
              type="text"
              class="chat-input"
              placeholder="Type a message..."
              @keydown.enter.prevent="sendMessage"
            />
            <button class="btn-send" @click="sendMessage" :disabled="!newMessage.trim()">Send</button>
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMessagesStore } from '../stores/messages'
import { mockConversations, mockMessages } from '../data/mockMessages'
import './MessagesView.css'

const auth = useAuthStore()
const messagesStore = useMessagesStore()
const route = useRoute()

const activeConvo = ref(null)
const newMessage = ref('')
const messagesEl = ref(null)
const loadingConvos = ref(false)
const loadingMessages = ref(false)
const isMobile = computed(() => window.innerWidth < 700)
let pollTimer = null

const currentUserId = computed(() => {
  const u = auth.user
  if (!u) return null
  const raw = u.id ?? u.userId
  if (raw == null || raw === '') return null
  const n = Number(raw)
  return Number.isNaN(n) ? null : n
})
const conversations = computed(() => messagesStore.conversations)
const currentMessages = computed(() => messagesStore.currentMessages)
const pageError = ref('')

function senderIdOf(msg) {
  if (!msg) return null
  const raw = msg.senderId ?? msg.sender_id
  if (raw == null || raw === '') return null
  const n = Number(raw)
  return Number.isNaN(n) ? null : n
}

function isMine(msg) {
  const sid = senderIdOf(msg)
  const uid = currentUserId.value
  if (sid == null || Number.isNaN(sid) || uid == null || Number.isNaN(uid)) return false
  return sid === uid
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
}

async function openConversation(convo) {
  pageError.value = ''
  activeConvo.value = convo
  loadingMessages.value = true
  try {
    await messagesStore.fetchMessages(convo.user.id)
    if (messagesStore.error) {
      pageError.value = messagesStore.error
    }
  } catch {
    messagesStore.currentMessages = mockMessages.filter(
      m => m.senderId === convo.user.id || m.receiverId === convo.user.id
    )
  } finally {
    loadingMessages.value = false
    await nextTick()
    scrollToBottom()
  }
}

function startPolling() {
  stopPolling()
  pollTimer = setInterval(() => {
    if (!activeConvo.value?.user?.id || document.hidden) return
    messagesStore.pollMessages(activeConvo.value.user.id)
  }, 4000)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || !activeConvo.value) return
  const content = newMessage.value.trim()
  newMessage.value = ''
  pageError.value = ''
  try {
    await messagesStore.sendMessage(activeConvo.value.user.id, content)
  } catch (e) {
    pageError.value = messagesStore.error || e?.response?.data?.error || 'Could not send message'
    messagesStore.currentMessages.push({
      id: Date.now(),
      senderId: currentUserId.value,
      receiverId: activeConvo.value.user.id,
      content,
      createdAt: new Date().toISOString(),
      edited: false
    })
  }
  await nextTick()
  scrollToBottom()
}

function scrollToBottom() {
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

watch(currentMessages, async () => {
  await nextTick()
  scrollToBottom()
})

async function openFromQueryUserId() {
  const userId = route.query.user
  if (!userId) return
  const convo = conversations.value.find(c => String(c.user.id) === String(userId))
  if (convo) {
    await openConversation(convo)
    return
  }
  // Mutual match exists but sidebar empty / query-only navigation: still try to load thread
  pageError.value = ''
  activeConvo.value = {
    id: `q-${userId}`,
    user: { id: Number(userId), firstName: '', lastName: '', photo: null },
    lastMessage: '',
    lastMessageAt: null,
    unread: 0,
  }
  loadingMessages.value = true
  try {
    await messagesStore.fetchMessages(Number(userId))
    if (messagesStore.error) {
      pageError.value = messagesStore.error
      activeConvo.value = null
    } else {
      try {
        await messagesStore.fetchConversations()
        const c = messagesStore.conversations.find(x => String(x.user.id) === String(userId))
        if (c) activeConvo.value = c
      } catch { /* keep synthetic convo */ }
    }
  } catch (e) {
    pageError.value = e?.response?.data?.error || 'You can only message mutual matches.'
    activeConvo.value = null
  } finally {
    loadingMessages.value = false
  }
}

onMounted(async () => {
  loadingConvos.value = true
  try {
    await messagesStore.fetchConversations()
  } catch {
    messagesStore.conversations = mockConversations
  } finally {
    loadingConvos.value = false
  }

  await openFromQueryUserId()

  startPolling()
})

watch(
  () => route.query.user,
  async (userId, prev) => {
    if (String(userId || '') === String(prev || '')) return
    await openFromQueryUserId()
  }
)

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

.messages-page {
  min-height: 100vh;
  background: #fff5f0;
  padding-top: 64px;
}

.messages-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  height: calc(100vh - 64px);
}

/* Sidebar */
.convo-sidebar {
  background: white;
  border-right: 1px solid #f0eaf6;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f0eaf6;
}

.sidebar-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;
  color: #1a1025;
  margin: 0;
}

.convo-error {
  margin: 0 1.25rem 0.75rem;
  padding: 0.65rem 0.85rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: #c0384d;
  background: rgba(232, 93, 117, 0.08);
  border: 1px solid rgba(232, 93, 117, 0.25);
  border-radius: 10px;
}

.convo-list { list-style: none; padding: 0; margin: 0; overflow-y: auto; flex: 1; }

.convo-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.9rem 1.25rem;
  cursor: pointer;
  border-bottom: 1px solid #f8f2fc;
  transition: background 0.15s;
}

.convo-item:hover { background: #fdf5f8; }
.convo-item.active { background: rgba(232, 93, 117, 0.06); }

.convo-avatar {
  width: 46px; height: 46px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid transparent;
}

.convo-item.active .convo-avatar { border-color: #e85d75; }

.convo-info { flex: 1; min-width: 0; }

.convo-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  color: #1a1025;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.convo-last {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #8b7fa0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.convo-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.3rem;
  flex-shrink: 0;
}

.convo-time {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: #b0a0c0;
}

.unread-badge {
  background: #e85d75;
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  width: 18px; height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Chat panel */
.chat-panel {
  display: flex;
  flex-direction: column;
  background: #fdfbfe;
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  font-size: 0.95rem;
}

.chat-empty span { font-size: 3rem; }

.chat-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #f0eaf6;
}

.chat-avatar {
  width: 40px; height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e85d75;
}

.chat-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  color: #1a1025;
}

.back-btn {
  font-family: 'DM Sans', sans-serif;
  background: none;
  border: none;
  color: #e85d75;
  font-size: 0.88rem;
  cursor: pointer;
  padding: 0;
  margin-right: 0.25rem;
}

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.msg-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.15rem;
  max-width: 100%;
}

.msg-row.mine {
  align-items: flex-end;
}

.msg-sender-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.68rem;
  font-weight: 600;
  color: #b0a0c0;
  padding: 0 0.15rem;
}

.msg-row.mine .msg-sender-tag {
  color: #e85d75;
}

.msg-bubble {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  background: white;
  color: #1a1025;
  padding: 0.65rem 1rem;
  border-radius: 16px 16px 16px 4px;
  max-width: 65%;
  line-height: 1.5;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  align-self: flex-start;
}

.msg-row.mine .msg-bubble {
  align-self: flex-end;
  margin-left: auto;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border-radius: 16px 16px 4px 16px;
}

.msg-row:not(.mine) .msg-bubble {
  margin-right: auto;
}

.msg-edited {
  font-size: 0.72rem;
  opacity: 0.65;
  margin-left: 0.35rem;
}

.msg-time {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: #b0a0c0;
  align-self: flex-start;
}

.msg-row.mine .msg-time {
  align-self: flex-end;
}

/* Input */
.chat-input-row {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: white;
  border-top: 1px solid #f0eaf6;
}

.chat-input {
  flex: 1;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  padding: 0.7rem 1rem;
  border: 1.5px solid #e8dff0;
  border-radius: 12px;
  outline: none;
  background: #fdfbfe;
  color: #1a1025;
  transition: border-color 0.2s;
}

.chat-input:focus { border-color: #e85d75; }

.btn-send {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  font-size: 0.9rem;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.7rem 1.4rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-send:hover:not(:disabled) { opacity: 0.88; }
.btn-send:disabled { opacity: 0.5; cursor: not-allowed; }

/* Misc */
.loading-mini { padding: 1.5rem; display: flex; justify-content: center; }
.loading-mini.center { flex: 1; align-items: center; }

.no-convos {
  padding: 2rem 1.5rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #8b7fa0;
  text-align: center;
  line-height: 1.6;
}

.spinner-sm {
  width: 24px; height: 24px;
  border: 2px solid rgba(232, 93, 117, 0.2);
  border-top-color: #e85d75;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 700px) {
  .messages-layout { grid-template-columns: 1fr; }
  .convo-sidebar.hidden, .chat-panel.hidden { display: none; }
}
</style>