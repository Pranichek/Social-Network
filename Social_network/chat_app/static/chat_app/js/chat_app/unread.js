const headerUnreadCount = document.querySelector("#headerUnreadCount");
const personalUnreadCount = document.querySelector("#personalUnreadCount");
const groupUnreadCount = document.querySelector("#groupUnreadCount");

// для текущих загруженных карточек, потому что остальные мы загружаем через пагинацию
let lastUnreadData = null;

function unreadText(element, count) {
    if (count == 0){
        element.parentElement.classList.add("hidden")
    }else{
        if (element.parentElement.classList.contains("hidden")){
            element.parentElement.classList.remove("hidden")
        }
    }
    return count;
}

function setUnreadText(element, count) {
    if (element) {
        element.textContent = unreadText(element, count);
    }
}

// function updateChatButton(chat) {
//     const button = document.querySelector(`[data-chat-id="${chat.id}"]`);
//     if (!button) return;

//     const lastMessage = button.querySelector(".bottom-data p");
//     if (lastMessage) {
//         lastMessage.textContent = chat.last;
//     }

//     if (chat.unread > 0) {
//         button.classList.add("chat-has-unread");
//         // Показуємо лічильник на картці
//         let badge = button.querySelector(".unread-badge");
//         if (!badge) {
//             badge = document.createElement("span");
//             badge.classList.add("unread-badge");
//             button.querySelector(".bottom-data").appendChild(badge);
//         }
//         badge.textContent = chat.unread;
//     } else {
//         button.classList.remove("chat-has-unread");
//         const badge = button.querySelector(".unread-badge");
//         if (badge) badge.remove();
//     }
// }

function updateChatButton(chat) {
    const button = document.querySelector(`[data-chat-id="${chat.id}"]`);
    if (!button) return;

    const lastMessage = button.querySelector(".last-message-text");
    if (lastMessage) {
        lastMessage.textContent = chat.last;
    }

    const timeEl = button.querySelector(".card-time");
    if (timeEl && chat.last_time) {
        timeEl.textContent = window.formatMessageTime(chat.last_time);
    }

    if (chat.unread > 0) {
        button.classList.add("chat-has-unread");

        // card.querySelector(".avatar-wrapper").insertAdjacentHTML('beforeend', `
        //     <span class="indicator-avatar">
        //         <p>1</p>
        //     </span>
        // `)

        // let badge = button.querySelector(".unread-badge");
        let badge = button.querySelector(".indicator-avatar");
        let badgeText = null
        button.classList.add("chat-has-unread");
        
        if (!badge) {
            
            badge = document.createElement("span");
            badge.classList.add("indicator-avatar");
            badgeText = document.createElement("p")

            badge.appendChild(badgeText)
            
            button.querySelector(".avatar-wrapper").appendChild(badge);
        }else{
            badgeText = badge.querySelector("p")
        }
        
        badgeText.textContent = chat.unread;
        
        // Переміщуємо картку вгору
        const list = button.parentElement;
        list.prepend(button);
    } else {
        button.classList.remove("chat-has-unread");
        const badge = button.querySelector(".indicator-avatar");
        if (badge) badge.remove();
    }
}

function showUnreadData(data) {
    lastUnreadData = data;
    setUnreadText(headerUnreadCount, data.total);
    setUnreadText(personalUnreadCount, data.personal_total);
    setUnreadText(groupUnreadCount, data.group_total);
    data.chats.forEach((chat) => {
        updateChatButton(chat);
    });
}

// делаем глобальной
window.reapplyUnreadData = function() {
    if (lastUnreadData) {
        showUnreadData(lastUnreadData);
    }
}

const unreadSocket = new WebSocket(`ws://${window.location.host}/chat/unread/`);
unreadSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    showUnreadData(data);
};

function updateUnreadData() {
    if (unreadSocket.readyState == WebSocket.OPEN) {
        unreadSocket.send("{}");
    }
}

window.updateUnreadData = updateUnreadData;

function checkMessages() {
    const endicatorMessage = document.querySelector(".endicator-messages")
    if (!endicatorMessage) return
    endicatorMessage.classList.add("hidden")
}

window.checkMessages = checkMessages