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

allButtons.forEach(button => {
    button.addEventListener('click', async () => {
        elementsForFriends.forEach(element => {
            if (element && !element.classList.contains('hidden')) {
                element.classList.toggle("hidden")
            }
        })
        
        if (profileBlock) {
            profileBlock.classList.toggle("hidden")
        }

        const idPerson = button.value
        
        const responseData = await fetch(`user_data/?user_id=${idPerson}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        
        if (responseData.ok) {
            const dataInfo = await responseData.json()
            document.querySelector(".username-card").textContent = dataInfo.user_data.pseudonym
            document.querySelector(".nickname").textContent = dataInfo.user_data.username
            document.querySelector(".number-posts").textContent = dataInfo.user_data.count_posts
            document.querySelector(".number-friends").textContent = dataInfo.user_data.count_friends

            const delBtn = document.getElementById("delete-btn")
            if (delBtn) {
                delBtn.value = idPerson
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
})