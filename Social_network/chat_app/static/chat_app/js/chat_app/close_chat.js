const closeChat = document.getElementById('close-chat');

const headerChats = document.getElementById('header-chat');
const mainText = document.getElementById('main-text');
const bottomPart = document.getElementById('chat-window');
const allElements = [headerChats, mainText, bottomPart];

const mainBlock = document.querySelector('.texting-box');


function showMainPrevview(){
    allElements.forEach((element) => {
        element.classList.toggle('hidden')
        window.clearCards()
    });
    if (mainBlock.classList.contains('show-chat')){
        mainBlock.classList.remove('show-chat')
    }
}

window.showMainPrevview = showMainPrevview

closeChat.addEventListener('click', (event) => {
    if (chatSocket) {
        chatSocket.close()
        chatSocket = null
    }
    currentChatId = null

    showMainPrevview()
})

