const closeChat = document.getElementById('close-chat');

const headerChats = document.getElementById('header-chat');
const mainText = document.getElementById('main-text');
const bottomPart = document.getElementById('chat-window');
const allElements = [headerChats, mainText, bottomPart];

const mainBlock = document.querySelector('.texting-box');



closeChat.addEventListener('click', (event) => {

    allElements.forEach((element) => {
        element.classList.toggle('hidden')
    });
    if (mainBlock.classList.contains('show-chat')){
        mainBlock.classList.remove('show-chat')
    }
})

