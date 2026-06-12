let currentChatMembers = []
let isCurrentChatGroup = false
let onlineMemberCount = 0

const statusSocket = new WebSocket(`ws://${window.location.host}/ws/status/`)

statusSocket.onmessage = function(event){
    const data = JSON.parse(event.data)

    if (data.action == 'statuc_update'){
        const userId = Number(data.user_id)

        if (currentChatId != null && currentChatMembers.includes(userId)){
            if (isCurrentChatGroup){
                document.querySelector(".status-chat").textContent = `${data.count_online} в мережі`
            }
        }else{
            const statusText = data.status == "online" ? 'в мережі' : 'не в мережі'
            document.querySelector(".status-chat").textContent = statusText
        }
    }
}