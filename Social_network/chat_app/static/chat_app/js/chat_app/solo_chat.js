
let chatSocket = null

const CSRFToken = document.querySelector('meta[name="csrf-token"]').content
const chatTitle = document.getElementById('title-chat')
const chatStatus = document.getElementById('chat-status')
const chatButtons = document.querySelectorAll('.card-contact')
const chatWindow = document.querySelector("#chat-window")
const messages = document.querySelector("#messeages")
const messageForm = document.querySelector("#messeage-form")
const messageInput = document.getElementById("messeage-input")


function scrollToBottom() {
    const messagesContainer = document.getElementById("messeages")
    messagesContainer.scrollTop = messagesContainer.scrollHeight
}



async function openChatWithUser(userId, username) {

    const response = await fetch(`/chat/chat_with/${userId}/`, {
        method: 'POST',
        headers: {'X-CSRFToken': CSRFToken},
    })

    const data = await response.json()
    
    document.querySelector("#main-text").classList.add("hidden")
    
    if (data.success){
        chatTitle.textContent = username
        activeChatId = data.chat_id          
        currentChatPage = 1                 
        isChatLoading = false                
        
        chatObserver.disconnect()        
        messages.innerHTML = '<div id="chat-load-sentinel" style="height: 1px;"></div>'
        messages.innerHTML += data.html

        chatWindow.classList.add("is-open")
        document.querySelector(".header-chat").classList.remove("hidden")
        chatWindow.classList.remove('hidden')
        document.querySelector(".texting-box").classList.add("show-chat")

        scrollToBottom()

        chatSentinel = document.getElementById("chat-load-sentinel")
        if (chatSentinel) {
            chatObserver.observe(chatSentinel)
        }

        InsertChatCard(userId, data.chat_card_html)
        
        connectWebSocket(data.chat_id)
    }
}

function InsertChatCard(userId, cardUser){
    const messageListContainer = document.querySelector('.message-cont .message-list')
    const existCard = messageListContainer.querySelector(`.block-card[data-chat-user="${userId}"]`)

    if (!existCard){
        const emptyText = messageListContainer.querySelector('p')
        if (emptyText){
            emptyText.remove()
        }
        
        messageListContainer.insertAdjacentHTML('beforeend', cardUser)
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
            // messageElement.classList.add("message")
            // messageElement.textContent = `${data.sender}: ${data.message_text}`

            const checkReadIconPath = '/static/chat_app/images/chat_images/check_read.svg'

            messageElement.innerHTML += `
                <div class="message">
                    <div class="message-outline">
                        <div class="msg-text">
                            <p>${data.message_text}</p>
                        </div>
                        
                        <div class="data-message">
                            <p>10:01</p>
                            <img src= "${checkReadIconPath}" alt="check_read">
                        </div>
                    </div>
                </div>
            `

            messages.appendChild(messageElement)
            scrollToBottom()
        }
    }
}

document.addEventListener('click', async (event) => {
    const chatElement = event.target.closest(".card-contact, .block-card")
    
    if (chatElement){
        const userId = chatElement.dataset.chatUser
        const userUsername = chatElement.dataset.chatUsername

        if (userId && userUsername){
            await openChatWithUser(userId, userUsername)
        }
    }
})



messageForm.addEventListener('submit', (event) => {
    event.preventDefault()
    const messageText = messageInput.value.trim()
    if (messageText){
        chatSocket.send(JSON.stringify({messageText: messageText}))
        messageInput.value = ""
    }
})