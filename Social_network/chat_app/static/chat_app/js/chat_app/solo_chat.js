
let chatSocket = null
let currentChatId = null

let isCurrentChatGroup = false
let currentChatMembers = []

const CSRFToken = document.querySelector('meta[name="csrf-token"]').content
const chatTitle = document.getElementById('title-chat')
const chatWindow = document.querySelector("#chat-window")
const messageForm = document.querySelector("#messeage-form")
const messageInput = document.getElementById("messeage-input")

function changeStatus(isGroup, members){
  isCurrentChatGroup = isGroup
  currentChatMembers = members || []

  const statusLabel = document.querySelector(".status-chat")
  if (!statusLabel) return

  if (isCurrentChatGroup) {
      let onlineCount = 0
      currentChatMembers.forEach(id => {
          if (window.onlineUsers && window.onlineUsers.has(String(id))) {
              onlineCount++
          }
      })
      statusLabel.textContent = `${currentChatMembers.length} учасників, ${onlineCount} в мережі`
  } else {
      const otherUserId = currentChatMembers[0]
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
      
      const messageElement = renderMessage(data, data.sender, isCurrentChatGroup)
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
    isCurrentChatGroup = data.is_group
    currentChatMembers = data.chat_members
    onlineMemberCount = data.online_count

    changeStatus(data.is_group, data.chat_members)

    chatTitle.textContent = chatName
    chatWindow.classList.add("is-open")
    document.querySelector("#header-chat").classList.remove("hidden")
    chatWindow.classList.remove('hidden')
    document.querySelector(".texting-box").classList.add("show-chat")

    connectWebSocket(data.chat_id)
    resetMessages(data.chat_id)
    await loadMessages()
    startObserver()
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
    isCurrentChatGroup = data.is_group
    currentChatMembers = data.chat_members

    changeStatus(data.is_group, data.chat_members)

    chatTitle.textContent = username
    chatWindow.classList.add("is-open")
    document.querySelector("#header-chat").classList.remove("hidden")
    chatWindow.classList.remove('hidden')
    document.querySelector(".texting-box").classList.add("show-chat")
    InsertChatCard(userId, data.chat_card_html)
    window.recheckCard()
    connectWebSocket(data.chat_id)
    resetMessages(data.chat_id)
    await loadMessages()
    startObserver()
  }
}

document.addEventListener('click', async (event) => {
  const chatElement = event.target.closest(".card-contact, .block-card")

  if (chatElement) {
    const userId = chatElement.dataset.chatUser
    const chatId = chatElement.dataset.chatId
    const chatName = chatElement.dataset.chatUsername || chatElement.dataset.chatTitle

    if (userId) {
      await openChatWithUser(userId, chatName)
    } else if (chatId) {
      await openChatById(chatId, chatName)
    }
  }
})

// messageForm.addEventListener('submit', (event) => {
//   event.preventDefault()
//   const messageText = messageInput.value.trim()
//   if (messageText) {
//     chatSocket.send(JSON.stringify({ messageText: messageText }))
//     messageInput.value = ""
//   }
// })

messageForm.addEventListener('submit', async (event)=>{
  event.preventDefault();
  const messageText = messageInput.value.trim();
  if (!messageText && !window.hasSelectedImages()){
    return
  }

  if (window.hasSelectedImages()){
    const data = await window.sendMessageWithImages(messageText)
    
    if (data && !data.success){
      return
    }
    messageInput.value = ''
    window.clearSelectedImages()
  }else{
    chatSocket.send(JSON.stringify({ messageText: messageText }))
    messageInput.value = ""
  }
})