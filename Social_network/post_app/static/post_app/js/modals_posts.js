// const allModals = document.getElementById('modal-settings')

// allModals.forEach(modal => {
//     modal.addEventListener('click', () => {

//     })
// })

const postsContainer = document.getElementById('posts-container')
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')

// openButtons.forEach(openButton => {
//     openButton.addEventListener('click',() => {
//         const parentNode = openButton.parentNode
//         const currentModal = parentNode.querySelector("#modal-settings")
//         const deleteButton = currentModal.querySelector('.delete-post')
//         const postId = deleteButton.id

        
//         if (window.getComputedStyle(currentModal).display == 'none'){
//             currentModal.style.display = 'flex'
//         }

//         const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
//         const urlAdress = `${window.location.origin}/post/delete_post/`
//         const data = {post_id: postId}

//         console.log(data)

//         deleteButton.addEventListener('click', () => {
//             fetch(urlAdress, {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     'X-CSRFToken': csrfToken
//                 },
//                 body: JSON.stringify(data),
//             }).then(async (responce) => {
//                 const data = await responce.json()

//                 if (!responce.ok){
//                     throw data
//                 }

//                 return data
//             }).then((data) => {
//                 console.log(data)
//             }).catch((data) => {
//                 if (data.errors){
//                     console.log(data.errors)
//                 }
//             })
//         })
//         })
//     })


postsContainer.addEventListener('click', (event) => {
    if (event.target.closest('.settings-post')) {
        const outlineData = event.target.closest('.outline-data')
        if (outlineData) {
            const currentModal = outlineData.querySelector('.modal-settings')
            if (currentModal) {
                if (window.getComputedStyle(currentModal).display == 'none') {
                    currentModal.style.display = 'flex'
                } else {
                    currentModal.style.display = 'none'
                }
            }
        }
    }

    const deleteButton = event.target.closest('.delete-post')
    if (deleteButton) {
        const postId = deleteButton.id
        const urlAdress = `${window.location.origin}/post/delete_post/`
        const data = { post_id: postId }

        fetch(urlAdress, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data),
        }).then(async (response) => {
            const resData = await response.json()

            if (!response.ok) {
                throw resData
            }
            return resData
        }).then((response) => {
            if (response.success) {
                const postElement = deleteButton.closest('.cont-post')
                if (postElement) {
                    postElement.remove()
                }
            }
        }).catch((err) => {
            console.log(err)
        })
    }
})