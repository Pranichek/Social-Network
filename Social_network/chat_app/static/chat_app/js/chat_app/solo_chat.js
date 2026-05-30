let chatSocket = null

const CSRFToken = document.querySelector('meta[name="csrf-token"]').content
const chatTitle = document.getElementById('chat-title')
const chatStatus = document.getElementById('chat-status')
const chatButtons = document.querySelectorAll('.card-contact')


async function openChatWithUser(userId, username) {

    const response = await fetch(`/chat/chat_with/${userId}/`, {
        method: 'POST',
        headers: {'X-CSRFToken': CSRFToken},
    })

    const data = await response.json()
    
    if (data.success){
        chatTitle.textContent = `Чат з ${username}`
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
        console.log(data)
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