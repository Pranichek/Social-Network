// window.onlineUsers = new Set()
// const onlineSocket = new WebSocket(`ws://${window.location.host}/chat/online/`)

// onlineSocket.onmessage = function (event) {
//     const data = JSON.parse(event.data)
//     const userId = String(data.user_id)

//     console.log(userId, "uro")
//     if (data.status == "online") {
//         window.onlineUsers.add(userId)
//     } else {
//         window.onlineUsers.delete(userId)
//     }

//     if (typeof window.changeStatus == "function") {
//         window.changeStatus(window.isCurrentChatGroup, window.currentChatMembers)
//     }

//     const userCard = document.querySelector(`.block-card[data-chat-user="${userId}"]`)
//     if (!userCard) return

//     const statusIndicator = userCard.querySelector('.status-indicator')
//     if (statusIndicator) {
//         if (data.status == "online") {
//             statusIndicator.classList.add("online")
//         } else {
//             statusIndicator.classList.remove("online")
//         }
//     }
// }

window.onlineUsers = new Set()


function applyOnlineStatuses(root = document) {
    root.querySelectorAll('[data-user-id]').forEach(card => {
        const userId = card.dataset.userId
        const indicator = card.querySelector('.status-indicator')
        if (!indicator) return

        if (window.onlineUsers.has(userId)) {
            indicator.classList.add("online")
        } else {
            indicator.classList.remove("online")
        }
    })
}
window.applyOnlineStatuses = applyOnlineStatuses

const onlineSocket = new WebSocket(`ws://${window.location.host}/chat/online/`)

onlineSocket.onmessage = function (event) {
    const data = JSON.parse(event.data)
    const userId = String(data.user_id)

    if (data.status == "online") {
        window.onlineUsers.add(userId)
    } else {
        window.onlineUsers.delete(userId)
    }

    if (typeof window.changeStatus == "function") {
        window.changeStatus(window.isCurrentChatGroup, window.currentChatMembers)
    }

    document.querySelectorAll(`[data-user-id="${userId}"]`).forEach(card => {
        const indicator = card.querySelector('.status-indicator')
        if (!indicator) return
        indicator.classList.toggle("online", data.status == "online")
    })
}