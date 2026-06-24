let chatSocket = null
let currentChatId = null

window.isCurrentChatGroup = false
window.currentChatMembers = []

const CSRFToken = document.querySelector('meta[name="csrf-token"]').content
const chatTitle = document.getElementById('title-chat')
const chatWindow = document.querySelector("#chat-window")
const messageForm = document.querySelector("#messeage-form")
const messageInput = document.getElementById("messeage-input")

function changeStatus(isGroup, members){
  window.isCurrentChatGroup = isGroup
  window.currentChatMembers = members || []

  const statusLabel = document.querySelector(".status-chat")
  if (!statusLabel) return

  if (window.isCurrentChatGroup) {
      let onlineCount = 0
      window.currentChatMembers.forEach(id => {
          if (window.onlineUsers && window.onlineUsers.has(String(id))) {
              onlineCount++
          }
      })
      statusLabel.textContent = `${window.currentChatMembers.length} учасників, ${onlineCount} в мережі`
  } else {
      const otherUserId = window.currentChatMembers[0]
      if (window.onlineUsers && window.onlineUsers.has(String(otherUserId))) {
          statusLabel.textContent = "в мережі"
      } else {
          statusLabel.textContent = "не в мережі"
      }
  }
}

window.changeStatus = changeStatus

function connectWebSocket(chatId) {
  if (chatSocket) {
    chatSocket.close()
  }

  currentChatId = chatId

  chatSocket = new WebSocket(`ws://${window.location.host}/chat/${chatId}/`)

  chatSocket.onmessage = function (event) {
    let data = JSON.parse(event.data)
    if (data.action == "chat_message") {
      console.log(data, "dfvdf")
      const messageElement = renderMessage(data, data.sender, window.isCurrentChatGroup)
      document.querySelector("#messeages").appendChild(messageElement)
      const messagesContainer = document.querySelector("#messeages")
      messagesContainer.scrollTop = messagesContainer.scrollHeight
      window.updateSeparators()
    }
  }
}

function InsertChatCard(userId, cardUser) {
  const messageListContainer = document.querySelector('.message-cont .message-list')
  const existCard = messageListContainer.querySelector(`.block-card[data-chat-user="${userId}"]`)

  if (!existCard) {
    messageListContainer.insertAdjacentHTML('beforeend', cardUser)
  }
}

async function openChatById(chatId, chatName) {
  const response = await fetch(`/chat/open/${chatId}/`, {
    method: 'GET',
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
  })

  currentChatId = chatId

  const data = await response.json()
  document.querySelector("#main-text").classList.add("hidden")

  if (data.success) {
    currentChatId = data.chat_id
    window.isCurrentChatGroup = data.is_group
    window.currentChatMembers = data.chat_members

    changeStatus(data.is_group, data.chat_members)

    chatTitle.textContent = chatName
    chatWindow.classList.add("is-open")
    document.querySelector("#header-chat").classList.remove("hidden")
    chatWindow.classList.remove('hidden')
    document.querySelector(".texting-box").classList.add("show-chat")

    connectWebSocket(data.chat_id)
    resetMessages(data.chat_id)
    window.updateUnreadData()
    await loadMessages()
    startObserver()

    const messagesContainer = document.querySelector("#messeages")
    if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight
  }
}

async function openChatWithUser(userId, username) {
  const response = await fetch(`/chat/chat_with/${userId}/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': CSRFToken },
  })

  const data = await response.json()
  document.querySelector("#main-text").classList.add("hidden")

  if (data.success) {
    currentChatId = data.chat_id
    window.isCurrentChatGroup = data.is_group
    window.currentChatMembers = data.chat_members

    changeStatus(data.is_group, data.chat_members)

    chatTitle.textContent = username
    chatWindow.classList.add("is-open")
    document.querySelector("#header-chat").classList.remove("hidden")
    chatWindow.classList.remove('hidden')
    document.querySelector(".texting-box").classList.add("show-chat")
    InsertChatCard(userId, data.chat_card_html)
    window.recheckCard()
    connectWebSocket(data.chat_id)
    window.updateUnreadData()
    resetMessages(data.chat_id)
    await loadMessages()
    startObserver()

    const messagesContainer = document.querySelector("#messeages")
    if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight
  }
}

let isSending = false

document.addEventListener('click', async (event) => {
  const chatElement = event.target.closest(".card-contact, .block-card")

  if (chatElement) {
    const userId = chatElement.dataset.chatUser
    const chatId = chatElement.dataset.chatId
    const chatType = chatElement.dataset.chatType
    const chatName = chatElement.dataset.chatUsername || chatElement.dataset.chatTitle

    if (chatType === 'solo') {
      await openChatWithUser(userId, chatName)
    } else if (chatType === 'group' || (chatId && !userId)) {
      await openChatById(chatId, chatName)
    } else if (userId) {
      await openChatWithUser(userId, chatName)
    }
  }
})
messageForm.addEventListener('submit', async (event) => {
  event.preventDefault()

  if (isSending) return

  const messageText = messageInput.value.trim()
  if (!messageText && !window.hasSelectedImages()) {
    return
  }

  isSending = true

  try {
    if (window.hasSelectedImages()) {
      const data = await window.sendMessageWithImages(messageText)
      if (data && !data.success) {
        return
      }
      messageInput.value = ''
      window.clearSelectedImages()
    } else {
      chatSocket.send(JSON.stringify({ 
        messageText: messageText,
        action: 'send_message'
      }))
      messageInput.value = ""
      
      const messagesContainer = document.querySelector("#messeages")
      if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight
    }
  } finally {
    const sendBtn = document.querySelector(".send-btn") 
    isSending = false
    if (sendBtn) sendBtn.disabled = false
  }
})