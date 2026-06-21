const notificationSocket = new WebSocket(`ws://${window.location.host}/chat/notifications/`)

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
            const endicatorMessage = document.querySelector(".endicator-messages")
            endicatorMessage.classList.remove("hidden")
            endicatorMessage.querySelector("p").textContent = '1'

            const card = document.querySelector(`.block-card[data-chat-id="${data.chat_id}"]`)
            if (card && !card.querySelector(".endicator-messages-bottom")) {
                card.classList.add("last-messages")
                card.querySelector(".bottom-data").insertAdjacentHTML('beforeend', `
                    <div class="endicator-messages-bottom">
                        <p style='color: #FFFFFF; font-size: 1.04vh; font-weight: 400;'>1</p>
                    </div>
                `)
                card.querySelector(".bottom-data").style.justifyContent = 'space-between'
            }
        }
    }

    if (data.action === "chat_card_update") {
        updateChatCardPreview(data)
    }
}

function updateChatCardPreview(data) {
    const card = document.querySelector(`.block-card[data-chat-id="${data.chat_id}"]`)

    if (!card) return

    const textEl = card.querySelector(".bottom-data p")
    const timeEl = card.querySelector(".card-time")

    if (textEl) {
        if (data.message_text) {
            textEl.textContent = data.message_text
        } else {
            textEl.textContent = 'Зображення'
        }
    }

    if (timeEl) timeEl.textContent = window.formatMessageTime(data.created_at)

    const list = card.parentElement
    list.prepend(card)
}