const arrowBack = document.querySelector(".arrow-cont")
const maintext = document.querySelector('#main-text')
const headerChat = document.querySelector(".header-chat")
const chatwindow = document.querySelector(".chat-window")
const textingBox = document.querySelector(".texting-box")

arrowBack.addEventListener('click', () => {
    maintext.classList.remove("hidden")
    textingBox.classList.toggle("show-chat")
    headerChat.classList.toggle("hidden")
    chatwindow.classList.toggle("hidden")
})