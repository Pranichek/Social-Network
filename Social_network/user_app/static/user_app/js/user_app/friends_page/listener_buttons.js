const allButtons = document.querySelectorAll("#button-card")
const sideMenu = document.getElementById('friends-nav')
const friendsMain = document.getElementById('friends-main')
const aloneSection = document.getElementById("section")
const elementsForFriends = [sideMenu, friendsMain, aloneSection]

const profileBlock = document.querySelector(".profile-block")

allButtons.forEach(button => {
    button.addEventListener('click',async () => {

        elementsForFriends.forEach(element => {
            if (!element.classList.contains('hidden')){
                element.classList.toggle("hidden")
            }
        })
        profileBlock.classList.toggle("hidden")

        const idPerson = button.value
        console.log(idPerson)
        const response = await fetch(`user_data/?user_id=${idPerson}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        const data = await response.json()

        document.querySelector(".username-card").textContent = data.user_data.pseudonym
        document.querySelector(".nickname").textContent = data.user_data.username
        document.querySelector(".number-posts").textContent = data.user_data.count_posts
        document.querySelector(".number-friends").textContent = data.user_data.count_friends
    })
})

