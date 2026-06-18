const notificationSocket = new WebSocket(`ws://${window.location.host}/chat/notifications/`)


function highlightChatCard(chatId, messageText, timeMessage) {
    console.log(chatId, "dlkfmlksmdfv")
    console.log(timeMessage)
    const card = document.querySelector(`.block-card[data-chat-user="${chatId}"]`)
    console.log(939848934)
    console.log(card)
    if (!card) return

    card.classList.add("last-messages")
    console.log(card.classList)

    const preview = card.querySelector(".bottom-data p")
    const dataMessage = card.querySelector(".top-data .card-time")
    if (preview && messageText) {
        preview.textContent = messageText
    }

    if (dataMessage){
        dataMessage.textContent = window.formatMessageTime(timeMessage)
    }

    const endicatorMessage = document.querySelector(".endicator-messages")
    endicatorMessage.classList.remove("hidden")
    const textMessage = endicatorMessage.querySelector("p")
    textMessage.textContent = '1'


    card.querySelector(".bottom-data").innerHTML += `
        <div class="endicator-messages-bottom">
            <p style='color: #FFFFFF; font-size: 1.04vh; font-weight: 400;'>1</p>
        </div>
    `

    const bottomData = card.querySelector(".bottom-data");
    bottomData.style.justifyContent = 'space-between';
}

function checkMessages(){
    const endicatorMessage = document.querySelector(".endicator-messages")
    const textMessage = Number(endicatorMessage.querySelector("p").textContent)
    if (textMessage == 1){
        endicatorMessage.classList.add("hidden")
    }
}

window.checkMessages = checkMessages

notificationSocket.onmessage = function(event) {
    const data = JSON.parse(event.data)
    if (data.action == "new_message_notification") {

        if (String(data.chat_id) != String(currentChatId)) {
            highlightChatCard(data.chat_id, data.message_text, data.created_at)
        }
    }
}