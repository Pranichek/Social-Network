const openModel = document.getElementById('settings-chat')
const settingsChat = document.getElementById('modal-settings')
const deleteChat = document.getElementById("delete-chat")


openModel.addEventListener('click', ()=>{
    settingsChat.classList.remove('hidden')
})

window.addEventListener('click', (event) => {
    const currentList = event.target.classList
    if (!currentList.contains("settings-chat")){
        if (!currentList.contains('modal-settings') && !settingsChat.classList.contains('hidden')){
            settingsChat.classList.add('hidden')
        }
    }
})

async function deleteChatfromDB(chatId){
    const response = await fetch(`/chat/delete/${chatId}/`, {
    method: 'GET',
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
  })

  const data = await response.json()

  if (data.success) {
    window.showMainPrevview()
  }
}

function deleteCardUser(chatId){
    const allCards = document.querySelectorAll(".block-card")

    allCards.forEach(card => {
        if (Number(card.dataset.chatUser) == Number(chatId)){
            card.remove()
            return false;
        }
    })
}

deleteChat.addEventListener('click',async () => {
    await deleteChatfromDB(currentChatId)
    deleteCardUser(currentChatId)
})

