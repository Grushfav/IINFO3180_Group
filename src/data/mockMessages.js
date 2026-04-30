export const mockMessages = [
  {
    id: 1,
    senderId: 1,
    receiverId: 4,
    content: 'Hey! How are you doing?',
    createdAt: '2026-04-01T10:00:00Z',
    edited: false
  },
  {
    id: 2,
    senderId: 4,
    receiverId: 1,
    content: 'Hi! I am doing great, thanks for asking!',
    createdAt: '2026-04-01T10:05:00Z',
    edited: false
  },
  {
    id: 3,
    senderId: 1,
    receiverId: 4,
    content: 'Would you like to grab coffee sometime?',
    createdAt: '2026-04-01T10:10:00Z',
    edited: false
  },
  {
    id: 4,
    senderId: 4,
    receiverId: 1,
    content: 'That sounds great! I know a nice place in Kingston.',
    createdAt: '2026-04-01T10:15:00Z',
    edited: false
  }
]

export const mockConversations = [
  {
    id: 1,
    user: {
      id: 1,
      firstName: 'Alice',
      lastName: 'Wonder',
      photo: 'https://randomuser.me/api/portraits/women/1.jpg'
    },
    lastMessage: 'That sounds great! I know a nice place in Kingston.',
    lastMessageAt: '2026-04-01T10:15:00Z',
    unread: 0
  },
  {
    id: 2,
    user: {
      id: 5,
      firstName: 'Emma',
      lastName: 'Artist',
      photo: 'https://randomuser.me/api/portraits/women/4.jpg'
    },
    lastMessage: 'Hey! Love your profile!',
    lastMessageAt: '2026-04-02T12:00:00Z',
    unread: 1
  }
]