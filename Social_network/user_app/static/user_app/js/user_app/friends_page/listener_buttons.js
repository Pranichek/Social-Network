const allButtons = document.querySelectorAll(".button-card")
const sideMenu = document.getElementById('friends-nav')
const friendsMain = document.getElementById('friends-main')
const aloneSection = document.getElementById("section")
const elementsForFriends = [sideMenu, friendsMain, aloneSection]

const profileBlock = document.querySelector(".profile-block")
const profileAcceptButton = document.getElementById("accept-button")
const profileDeleteButton = document.getElementById("delete-button")

let currentAction = null
let currentId = null

function closeProfile() {
    profileBlock.classList.add("hidden")
    elementsForFriends.forEach(element => {
        element.classList.remove("hidden")
    })
    currentAction = null
    currentId = null
}

allButtons.forEach(button => {
    button.addEventListener('click', async () => {

        elementsForFriends.forEach(element => {
            if (!element.classList.contains('hidden')) {
                element.classList.add("hidden")
            }
        })

        profileBlock.classList.remove("hidden")

        currentUserId = button.value
        currentAction = button.dataset.action

        if (currentAction === "accepted") {
            profileAcceptButton.textContent = "Підтвердити"
        }

        else if (currentAction === "add") {
            profileAcceptButton.textContent = "Додати"
        }

        try {
            const response = await fetch(`user_data/?user_id=${currentUserId}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            const data = await response.json()

            document.querySelector(".username-card").textContent = data.user_data.pseudonym
            document.querySelector(".nickname").textContent = data.user_data.username
            document.querySelector(".number-posts").textContent = data.user_data.count_posts
            document.querySelector(".number-friends").textContent = data.user_data.count_friends

        } catch (error) {
            console.error('Error fetching user data:', error)
        }
    })
})

if (profileAcceptButton) {
    profileAcceptButton.addEventListener('click', async () => {

        if (!currentUserId || !currentAction) return;

        try {
            const response = await fetch(`/settings/friends/change_status/${currentAction}/?id=${currentUserId}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            const data = await response.json()

            if (data.success) {
                closeProfile()

                const card = document.querySelector(`.button-card[value="${currentUserId}"]`).closest('.profile-block');

                if (card) {
                    const card = cardButton.closest('.card') || cardButton.closest('div'); 
                    card.remove();
                }
            }

        } catch (error) {
            console.error(error)
        }
    })
}

if (profileDeleteButton) {
    profileDeleteButton.addEventListener('click', async () => {

        if (!currentUserId) return;

        try {
            const response = await fetch(`/settings/friends/change_status/desmissed/?id=${currentUserId}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            const data = await response.json()

            if (data.success) {
                closeProfile()

                const card = document.querySelector(`.button-card[value="${currentUserId}"]`).closest('.profile-block');

                if (card) {
                    card.remove();
                }
            }

        } catch (error) {
            console.error(error)
        }
    })
}