const delBtn = document.getElementById("delete-btn")
const acceptProfileBtn = document.querySelector(".accept-button")
const acceptModal = document.querySelector(".accept-action")
const acceptBtn = document.querySelector(".accept-btn")
const declineBtn = document.querySelector(".decline-btn")
const shadowModal = document.getElementById("shadow")

let pendingAction = null
let pendingUserId = null

function openModal(action, userId) {
    if (!userId) return
    
    pendingAction = action
    pendingUserId = userId

    if (acceptModal) acceptModal.classList.remove("hidden")
    
    if (shadowModal) {
        shadowModal.classList.remove("hidden")
        shadowModal.classList.add("active")
    }
}

function closeModal() {
    pendingAction = null
    pendingUserId = null
    
    if (acceptModal) acceptModal.classList.add("hidden")
    
    if (shadowModal) {
        shadowModal.classList.add("hidden")
        shadowModal.classList.remove("active")
    }
}

if (delBtn) {
    delBtn.addEventListener('click', () => {
        openModal('delete', delBtn.value)
    })
}

if (acceptProfileBtn) {
    acceptProfileBtn.addEventListener('click', () => {
        // Берем действие, которое мы сохранили при открытии профиля
        const action = acceptProfileBtn.getAttribute('data-action')
        
        // Открываем модалку только если действие есть
        if (action) {
            openModal(action, acceptProfileBtn.value)
        }
    })
}


if (declineBtn) {
    declineBtn.addEventListener('click', closeModal)
}

if (acceptBtn) {
    acceptBtn.addEventListener('click', async () => {
        if (!pendingUserId || !pendingAction) return
        
        acceptBtn.disabled = true

        const data = await window.friendShipStatus(pendingUserId, pendingAction)

        if (data && data.success) {
            closeModal()

            if (typeof profileBlock !== 'undefined' && profileBlock) {
                profileBlock.classList.add("hidden")
            }

            if (typeof elementsForFriends !== 'undefined') {
                elementsForFriends.forEach(element => {
                    if (element && element.classList.contains('hidden') && element.id !== 'section') {
                        element.classList.remove("hidden")
                    }
                })
            }

            if (typeof friendPostList !== 'undefined' && friendPostList) {
                friendPostList.innerHTML = ""
            }
            
            if (typeof friendSentinel !== 'undefined' && friendSentinel && typeof friendObserver !== 'undefined') {
                friendObserver.unobserve(friendSentinel)
            }

            const deletedUserCard = document.querySelector(`.person-card button[value="${pendingUserId}"]`)
            
            if (deletedUserCard) {
                const cardElement = deletedUserCard.closest('.person-card')
                if (cardElement) cardElement.remove()
            }

            if (pendingAction === 'accepted' && data.html) {                
                const friendsContainer = document.getElementById('cards-friends')
                if (friendsContainer) friendsContainer.insertAdjacentHTML('afterbegin', data.html)
            }
            
            if (pendingAction === 'delete' && data.html) {
                const recommendationsContainer = document.getElementById('cards-recommendations')
                if (recommendationsContainer) recommendationsContainer.insertAdjacentHTML('afterbegin', data.html)
            }
        }

        acceptBtn.disabled = false
    })
}