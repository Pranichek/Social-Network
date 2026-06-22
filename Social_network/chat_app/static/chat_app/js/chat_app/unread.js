const headerUnreadCount = document.querySelector("#headerUnreadCount");
const personalUnreadCount = document.querySelector("#personalUnreadCount");
const groupUnreadCount = document.querySelector("#groupUnreadCount");

function unreadText(count) {
    if (count == 0) return "";
    return `(${count})`;
}

function setUnreadText(element, count) {
    if (element) {
        element.textContent = unreadText(count);
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
        let badge = button.querySelector(".unread-badge");
        if (!badge) {
            badge = document.createElement("span");
            badge.classList.add("unread-badge");
            button.querySelector(".bottom-data").appendChild(badge);
        }
        badge.textContent = chat.unread;
        
        // Переміщуємо картку вгору
        const list = button.parentElement;
        list.prepend(button);
    } else {
        button.classList.remove("chat-has-unread");
        const badge = button.querySelector(".unread-badge");
        if (badge) badge.remove();
    }
}

function showUnreadData(data) {
    setUnreadText(headerUnreadCount, data.total);
    setUnreadText(personalUnreadCount, data.personal_total);
    setUnreadText(groupUnreadCount, data.group_total);
    data.chats.forEach((chat) => {
        updateChatButton(chat);
    });
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