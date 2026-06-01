let chatSocket = null

const CSRFToken = document.querySelector('meta[name="csrf-token"]').content
const chatTitle = document.getElementById('chat-title')
const chatStatus = document.getElementById('chat-status')
const chatButtons = document.querySelectorAll('.card-contact')
const chatWindow = document.querySelector("#chat-window")
const messages = document.querySelector("#messeages")
const messageForm = document.querySelector("#messeage-form")
const messageInput = document.getElementById("messeage-input")


async function openChatWithUser(userId, username) {

    const response = await fetch(`/chat/chat_with/${userId}/`, {
        method: 'POST',
        headers: {'X-CSRFToken': CSRFToken},
    })

    const data = await response.json()
    
    if (data.success){
        chatTitle.textContent = `Чат з ${username}`
        chatStatus.classList.add("hidden")
        messages.innerHTML = ""
        chatWindow.classList.add("is-open")
        connectWebSocket(data.chat_id)
    }
}

function connectWebSocket(chatId){
    if (chatSocket){
        chatSocket.close()
    }

    chatSocket = new WebSocket(`ws://${window.location.host}/chat/${chatId}/`)

    chatSocket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        
        if (data.action == "chat_message"){
            const messageElement = document.createElement("div")
            messageElement.classList.add("message")
            messageElement.textContent = `${data.sender}: ${data.message_text}`
            messages.appendChild(messageElement)
        }
    }
}

chatButtons.forEach(button => {
    button.addEventListener('click',async () => {
        await openChatWithUser(
            button.dataset.chatUser,
            button.dataset.chatUsername
        )
    })
});


messageForm.addEventListener('submit', (event) => {
    event.preventDefault()
    const messageText = messageInput.value.trim()
    if (messageText){
        chatSocket.send(JSON.stringify({messageText: messageText}))
        messageInput.value = ""
    }
})