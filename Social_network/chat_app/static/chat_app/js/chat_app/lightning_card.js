let rightCards = document.querySelectorAll('.block-card')
let contacts = document.querySelectorAll('.card-contact')
let currentId = null

function reloadDict(){
    rightCards = document.querySelectorAll('.block-card')
    contacts = document.querySelectorAll('.card-contact')
    listenerContacts()
    changeBg()
}
window.reloadDict = reloadDict

function clearCards(){
    rightCards.forEach((card) => {
        if (card.classList.contains('active')){
            card.classList.remove('active')
        }
        
    })
}

function changeBg(){
    rightCards.forEach((card) => {
        card.addEventListener('click', () => {
            clearCards()
            card.classList.add('active')
        })
    })
}

function recheckCard(cardId){
    rightCards.forEach((card) => {
        if (card.dataset.chatUser){
            if (card.dataset.chatUser === cardId){
                card.classList.add('active')
            }
        }
    })
}

window.recheckCard = recheckCard

changeBg()


// Контакти
function listenerContacts(){
    contacts.forEach((contactCard) => {
        contactCard.addEventListener('click', () => {
            clearCards()
            const idUser = contactCard.dataset.chatUser
            currentId = idUser
            console.log(idUser)
            rightCards.forEach((cardMessage) => {
                console.log(7)
                if (cardMessage.dataset.chatUser){
                    const checkId = cardMessage.dataset.chatUser
                    console.log(checkId, ";l,l;,l;fdv")
                    if (idUser == checkId){
                        cardMessage.classList.add('active')
                    }
                }
            })
            
        })
    })
}


listenerContacts()