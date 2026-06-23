let currentFriendPage = 1
let isFriendPostsLoading = false
let currentFriendId = null

const friendPostList = document.querySelector("#user-posts")
const friendSentinel = document.getElementById("post-load-sentinel")

const friendObserver = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && !isFriendPostsLoading && currentFriendId) {
        isFriendPostsLoading = true
        currentFriendPage++
        
        const response = await fetch(`friend_posts/?user_id=${currentFriendId}&page=${currentFriendPage}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        
        if (response.ok) {
            const data = await response.json()

            if (data.html && friendPostList) {
                friendPostList.insertAdjacentHTML("beforeend", data.html)
            }

            if (!data.has_next && friendSentinel) {
                friendObserver.unobserve(friendSentinel)
            }
        }

        isFriendPostsLoading = false
    }
}, { rootMargin: "200px" })

const allButtons = document.querySelectorAll("#button-card")
const sideMenu = document.getElementById('friends-nav')
const friendsMain = document.getElementById('friends-main')
const aloneSection = document.getElementById("section")
const elementsForFriends = [sideMenu, friendsMain, aloneSection]
const profileBlock = document.querySelector(".profile-block")

// allButtons.forEach(button => {
//     button.addEventListener('click', async () => {
//         elementsForFriends.forEach(element => {
//             if (element && !element.classList.contains('hidden')) {
//                 element.classList.toggle("hidden")
//             }
//         })
        
//         if (profileBlock) {
//             profileBlock.classList.toggle("hidden")
//         }

//         const idPerson = button.value
        
//         const responseData = await fetch(`user_data/?user_id=${idPerson}`, {
//             headers: { 'X-Requested-With': 'XMLHttpRequest' }
//         })
        
//         if (responseData.ok) {
//             const dataInfo = await responseData.json()
//             const userData = dataInfo.user_data 

//             const nameElement = document.querySelector('.profile-block .username-card')
//             const nickElement = document.querySelector('.profile-block .nickname')
//             const postsElement = document.querySelector('.profile-block .number-posts')
//             const friendsElement = document.querySelector('.profile-block .number-friends')

//             if (nameElement) nameElement.textContent = userData.username
//             if (nickElement) nickElement.textContent = userData.pseudonym
//             if (postsElement) postsElement.textContent = userData.count_posts
//             if (friendsElement) friendsElement.textContent = userData.count_friends

//             if (delBtn) delBtn.value = idPerson

//             if (acceptProfileBtn) {
//                 acceptProfileBtn.value = idPerson 
                
//                 if (button.classList.contains('add-btn')) {
//                     acceptProfileBtn.setAttribute('data-action', 'add')
//                     acceptProfileBtn.textContent = 'Додати' 
//                 } else if (button.classList.contains('accepted-btn')) {
//                     acceptProfileBtn.setAttribute('data-action', 'accepted')
//                     acceptProfileBtn.textContent = 'Підтвердити'
//                 } else {
//                     acceptProfileBtn.setAttribute('data-action', '')
//                 }
//             }
//         }

//         currentFriendId = idPerson
//         currentFriendPage = 1
//         isFriendPostsLoading = false
        
//         if (friendPostList) {
//             friendPostList.innerHTML = ""
//         }
        
//         if (friendSentinel) {
//             friendObserver.unobserve(friendSentinel)
//         }

//         const responsePosts = await fetch(`friend_posts/?user_id=${currentFriendId}&page=1`, {
//             headers: { 'X-Requested-With': 'XMLHttpRequest' }
//         })

//         if (responsePosts.ok) {
//             const dataPosts = await responsePosts.json()

//             if (dataPosts.html && friendPostList) {
//                 friendPostList.insertAdjacentHTML("beforeend", dataPosts.html)
                
//                 if (dataPosts.has_next && friendSentinel) {
//                     friendObserver.observe(friendSentinel)
//                 }
//             }
//         }
//     })
// })

// ВИкористовуємо делегірованіе подій, щоб натискання відслідковувалося навіть на кнопки, які були добавленні через пагінацію
document.addEventListener('click', async (event) => {
    console.log("lol")
    const button = event.target.closest('#button-card')
    if (!button) return


    elementsForFriends.forEach(element => {
        if (element && !element.classList.contains('hidden')) {
            element.classList.add("hidden") 
        }
    })
    
    if (profileBlock) {
        profileBlock.classList.remove("hidden")
    }

    const idPerson = button.value
    
    const responseData = await fetch(`user_data/?user_id=${idPerson}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    
    if (responseData.ok) {
        const dataInfo = await responseData.json()
        const userData = dataInfo.user_data

        const nameElement = document.querySelector('.profile-block .username-card')
        const nickElement = document.querySelector('.profile-block .nickname')
        const postsElement = document.querySelector('.profile-block .number-posts')
        const friendsElement = document.querySelector('.profile-block .number-friends')

        if (nameElement) nameElement.textContent = userData.username
        if (nickElement) nickElement.textContent = userData.pseudonym
        if (postsElement) postsElement.textContent = userData.count_posts
        if (friendsElement) friendsElement.textContent = userData.count_friends

        if (delBtn) delBtn.value = idPerson

        if (acceptProfileBtn) {
            acceptProfileBtn.value = idPerson
            
            if (button.classList.contains('add-btn')) {
                acceptProfileBtn.setAttribute('data-action', 'add')
                acceptProfileBtn.textContent = 'Додати' 
            } else if (button.classList.contains('accepted-btn')) {
                acceptProfileBtn.setAttribute('data-action', 'accepted')
                acceptProfileBtn.textContent = 'Підтвердити'
            } else {
                acceptProfileBtn.setAttribute('data-action', '')
            }
        }
    }

    currentFriendId = idPerson
    currentFriendPage = 1
    isFriendPostsLoading = false
    
    if (friendPostList) {
        friendPostList.innerHTML = ""
    }
    
    if (friendSentinel) {
        friendObserver.unobserve(friendSentinel)
    }

    const responsePosts = await fetch(`friend_posts/?user_id=${currentFriendId}&page=1`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })

    if (responsePosts.ok) {
        const dataPosts = await responsePosts.json()

        if (dataPosts.html && friendPostList) {
            friendPostList.insertAdjacentHTML("beforeend", dataPosts.html)
            
            if (dataPosts.has_next && friendSentinel) {
                friendObserver.observe(friendSentinel)
            }
        }
    }
})