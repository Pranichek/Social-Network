import { clearFields } from "./clear_form.js"

const linksDiv = document.querySelector("#links-list")
const createPostForm = document.getElementById('create-post')
const shadow = document.getElementById('shadow') 


function updateButtons() {
    const blocks = linksDiv.querySelectorAll('.input-block')
    
    blocks.forEach((block, index) => {
        const plusDiv = block.querySelector('.plus-div')
        
        if (index == blocks.length - 1) {
            if (!plusDiv) {
                const html = `
                    <div class="plus-div">
                        <img class="plus-icon add-new-link" src="/static/post_app/images/posts_images/plus-icon.svg" alt="+">
                    </div>
                `
                
                const crossDiv = block.querySelector('.cross-div')
                if (crossDiv) {
                    crossDiv.insertAdjacentHTML('beforebegin', html)
                } else {
                    block.insertAdjacentHTML('beforeend', html)
                }
            }
        } 
        else {
            if (plusDiv) {
                plusDiv.remove()
            }
        }
    })
}

linksDiv.addEventListener('click', (event) => {    
    if (event.target.closest('.add-new-link')) {
        const htmlBlock = `
            <div class="input-block">
                <input class="input-link" type="url" name="links" placeholder="Додайте посилання">
                <div class="plus-div">
                    <img class="plus-icon add-new-link" src="/static/post_app/images/posts_images/plus-icon.svg" alt="+">
                </div>
                <div class="cross-div">
                    <img class="cross-icon remove-link" src="/static/post_app/images/posts_images/plus-icon.svg" alt="x">
                </div>
            </div>
        `
        linksDiv.insertAdjacentHTML('beforeend', htmlBlock)
        updateButtons() 
    }

    if (event.target.closest('.remove-link')) {
        event.target.closest('.input-block').remove()
        updateButtons()
    }
})





document.getElementById('create-post').addEventListener('submit', function(event) {
    event.preventDefault()

    const form = event.target
    const formData = new FormData(form)
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')


    fetch(form.action, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData,
    }).then(async (responce) => {
        const data = await responce.json()

        if (!responce.ok){
            throw data
        }

        return data
    }).then((data) => {
        clearFields()
        createPostForm.classList.add('hidden')
        if (shadow) shadow.classList.add('hidden') 

        if (data.html) {
            const postsContainer = document.getElementById('posts-container')
            if (postsContainer) {
                postsContainer.insertAdjacentHTML('afterbegin', data.html)
            }
        }
    }).catch((data) => {
        if (data.errors){
            console.log(data.errors)
        }
    })
})