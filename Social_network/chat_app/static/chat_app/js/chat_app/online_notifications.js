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
        const checkHeader = document.querySelector(".header-chat")
        console.log(checkHeader.classList)
        if (String(data.chat_id) != String(currentChatId) || checkHeader.classList.contains("hidden")) {
            console.log("dada")
            const endicatorMessage = document.querySelector(".endicator-messages")
            endicatorMessage.classList.remove("hidden")

            endicatorMessage.querySelector("p").textContent = '1'

            const card = document.querySelector(`.block-card[data-chat-id="${data.chat_id}"]`)

            if (card && !card.querySelector(".indicator-avatar")) {
                card.classList.add("last-messages")
                card.querySelector(".avatar-wrapper").insertAdjacentHTML('beforeend', `
                    <span class="indicator-avatar">
                        <p>1</p>
                    </span>
                `)
            }else{
                const counter =  Number(card.querySelector(".indicator-avatar p").textContent) + 1
                card.querySelector(".indicator-avatar p").textContent = counter
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