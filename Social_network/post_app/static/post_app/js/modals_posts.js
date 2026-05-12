// const allModals = document.getElementById('modal-settings')

// allModals.forEach(modal => {
//     modal.addEventListener('click', () => {

//     })
// })

const openButtons = document.querySelectorAll('#settings-post')

openButtons.forEach(openButton => {
    openButton.addEventListener('click',() => {
        const parentNode = openButton.parentNode
        const currentModal = parentNode.querySelector("#modal-settings")
        const deleteButton = currentModal.querySelector('.delete-post')
        const postId = deleteButton.id

        
        if (window.getComputedStyle(currentModal).display == 'none'){
            currentModal.style.display = 'flex'
        }

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        const urlAdress = `${window.location.origin}/post/delete_post/`
        const data = {post_id: postId}

        console.log(data)

        deleteButton.addEventListener('click', () => {
            fetch(urlAdress, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data),
            }).then(async (responce) => {
                const data = await responce.json()

                if (!responce.ok){
                    throw data
                }

                return data
            }).then((data) => {
                console.log(data)
            }).catch((data) => {
                if (data.errors){
                    console.log(data.errors)
                }
            })
        })
        })
    })


