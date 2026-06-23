const friendRequestWebsocket = new WebSocket(`ws://${window.location.host}/ws/friend_requests/`)
const friendCount = document.getElementById('friendRequestCount')


friendRequestWebsocket.onmessage = function(event) {
    const data = JSON.parse(event.data)
    updateFriendCount(data.count)
}

function updateFriendCount(count){
    if (!friendCount) return

    if (count > 0){
        friendCount.textContent = count
        friendCount.parentElement.classList.remove('hidden')
    }else{
        friendCount.parentElement.classList.add('hidden')
    }
    
}