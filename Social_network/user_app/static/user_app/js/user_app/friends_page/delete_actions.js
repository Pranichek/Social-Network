const delBtn = document.getElementById("delete-btn")
const acceptModal = document.querySelector(".accept-action")
const acceptBtn = document.querySelector(".accept-btn")
const declineBtn = document.querySelector(".decline-btn")
const shadowModal = document.getElementById("shadow")


if (delBtn) {
    delBtn.addEventListener('click', () => {
        const idToDelete = delBtn.value
        
        if (!idToDelete) {
            console.error("ID нема")
            return
        }

        if (acceptModal) acceptModal.classList.remove("hidden")
        if (shadowModal) {
            shadowModal.classList.remove("hidden")
            shadowModal.classList.add("active")
        }

    })
}

if (declineBtn) {
    declineBtn.addEventListener('click', () => {
        if (acceptModal) acceptModal.classList.add("hidden")
        if (shadowModal) {
            shadowModal.classList.add("hidden")
            shadowModal.classList.remove("active")
        }
    })
}

if (acceptBtn) {
    acceptBtn.addEventListener('click', async () => {
        const idToDelete = delBtn.value
        
        acceptBtn.disabled = true

        const data = await window.friendShipStatus(idToDelete, 'delete')

        if (data && data.success) {
            if (acceptModal) acceptModal.classList.add("hidden")
            if (shadowModal) shadowModal.classList.add("hidden")

            if (profileBlock) profileBlock.classList.add("hidden")

            elementsForFriends.forEach(element => {
                if (element && element.classList.contains('hidden') && element.id != 'section') {
                    element.classList.remove("hidden")
                }
            })

            if (friendPostList) {
                friendPostList.innerHTML = ""
            }
            
            if (friendSentinel && typeof friendObserver != 'undefined') {
                friendObserver.unobserve(friendSentinel)
            }

            const deletedUserCard = document.querySelector(`.person-card button[value="${idToDelete}"]`)
            if (deletedUserCard) {
                const cardElement = deletedUserCard.closest('.person-card')
                if (cardElement) cardElement.remove()
            }
        }

        acceptBtn.disabled = false
    })
}