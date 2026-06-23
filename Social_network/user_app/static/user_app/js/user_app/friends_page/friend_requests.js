// const friendRequestWebsocket = new WebSocket(`ws://${window.location.host}/ws/friend_requests/`)
// const friendCount = document.getElementById('friendRequestCount')


// friendRequestWebsocket.onmessage = function(event) {
//     const data = JSON.parse(event.data)
//     updateFriendCount(data.count)
// }

// function updateFriendCount(count){
//     if (!friendCount) return

//     if (count > 0){
//         friendCount.textContent = count
//         friendCount.parentElement.classList.remove('hidden')
//     }else{
//         friendCount.parentElement.classList.add('hidden')
//     }
    
// }

const friendRequestWebsocket = new WebSocket(`ws://${window.location.host}/ws/friend_requests/`)
const friendCount = document.getElementById('friendRequestCount')


friendRequestWebsocket.onmessage = function(event) {
    const data = JSON.parse(event.data)

    if (data.type === 'count_update') {
        updateFriendCount(data.count)
    }

    if (data.type === 'new_request') {
        handleNewFriendRequest(data.from_user_id)
    }
}

function updateFriendCount(count) {
    if (!friendCount) return

    if (count > 0) {
        friendCount.textContent = count
        friendCount.parentElement.classList.remove('hidden')
    } else {
        friendCount.parentElement.classList.add('hidden')
    }
}

async function handleNewFriendRequest(fromUserId) {
    console.log('handleNewFriendRequest called', fromUserId)

    // Ищем контейнер карточек запросов напрямую по id
    const sectionList = document.getElementById('cards-requests')
    if (!sectionList) return  // не на странице друзей

    // Убираем карточку из рекомендаций если там есть
    const existingCard = document.querySelector(`.person-card[data-user-id="${fromUserId}"]`)
    if (existingCard) existingCard.remove()

    // Получаем готовую карточку с бэка
    const response = await fetch(`/settings/friends/card/?user_id=${fromUserId}&section=requests`)
    const data = await response.json()

    sectionList.insertAdjacentHTML('afterbegin', data.html)
}