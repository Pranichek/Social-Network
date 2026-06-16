const notificationSocket = new WebSocket(`ws://${window.location.host}/chat/notifications/`);


notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(989838949384)
    console.log(data.action)
    if (data.action == "new_message") {
        const chatCard = document.querySelector(`.block-card[data-chat-user="${data.chat_id}"]`);
        console.log(data.chat_id)
        console.log(chatCard)
        
        if (chatCard) {
            chatCard.classList.add('has-new-message');
            chatCard.classList.add('active');
            
            const preview = chatCard.querySelector('.last-message-text');
            if (preview) preview.textContent = data.text;
            
            document.querySelector('#message-block-cards').prepend(chatCard);
        }
    }
};