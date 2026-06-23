const createTagModal = document.querySelector('.create-tag')
const createPostForm = document.getElementById('create-post')
const addCustomTagBtn = document.querySelector('#add-custom-tag')
const saveTagBtn = document.getElementById('save-button')
const cancelTagBtn = document.getElementById('cancel-button')
const newTagInput = document.getElementById('new-tag-input')
const customTagsDiv = document.getElementById('custom-tags')

const closeBtns = document.querySelectorAll('.close-form-btn')
const shadow = document.getElementById('shadow') 
const openFormBtn = document.getElementById('show-form') 

let tags = document.querySelectorAll('.custom-tag-label')


if (openFormBtn) {
    openFormBtn.addEventListener('click', () => {
        createPostForm.classList.remove('hidden')
        if (shadow) shadow.classList.remove('hidden')
    })
}

closeBtns.forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
        createPostForm.classList.add('hidden') 
        createTagModal.classList.add('hidden') 
        if (shadow) shadow.classList.add('hidden') 
    })
})

if (shadow) {
    shadow.addEventListener('click', () => {
        createPostForm.classList.add('hidden') 
        createTagModal.classList.add('hidden') 
        shadow.classList.add('hidden') 
    })
}

addCustomTagBtn.addEventListener('click', () => {
    createPostForm.classList.add('hidden') 
    createTagModal.classList.remove('hidden') 
    newTagInput.value = ''
})

cancelTagBtn.addEventListener('click', (event) => {
    event.preventDefault()
    createTagModal.classList.add('hidden') 
    createPostForm.classList.remove('hidden') 
})

saveTagBtn.addEventListener('click', (e) => {
    e.preventDefault()
    const tagValue = newTagInput.value.trim()

    if (tagValue) {
        const newTagHtml = `
            <div class="custom-tag-label">
                <input type="checkbox" name="custom_tags" value="${tagValue}" checked style="display:none">
                <span class="tag-pill">#${tagValue}</span>
            </div>
        `
        tags = document.querySelectorAll('.custom-tag-label')
        customTagsDiv.insertAdjacentHTML('beforeend', newTagHtml)
    }

    createTagModal.classList.add('hidden')
    createPostForm.classList.remove('hidden')
})

const tagsContainer = document.querySelector('.tags-container')

tagsContainer.addEventListener('click', (element) => {
    const tagElement = element.target.closest('.custom-tag-label')
    // если нажали клик бл не по тегу
    if (!tagElement) return

    const checkInput = tagElement.querySelector("input[type='checkbox']")

    const tagsList = document.querySelector(".show-tags")
    const tagText = tagElement.textContent.trim()

    if (tagElement.classList.contains('active-tag')) {
        tagElement.classList.remove('active-tag') 
        if (checkInput) {
            checkInput.checked = false 
        }
        
        const paragraphs = tagsList.querySelectorAll('p')
        paragraphs.forEach(p => {
            if (p.textContent == tagText) {
                p.remove()
            }
        })

    } else {        
        tagElement.classList.add('active-tag') 
        if (checkInput) {
            checkInput.checked = true 
        }
        
        const paragraph = document.createElement('p')
        paragraph.textContent = tagText
        tagsList.append(paragraph)
    }
})
// tags.forEach(tag =>{
//     tag.addEventListener('click', () => {
//         const checkInput = tag.querySelector("input[type='checkbox']")
//         if (tag.classList.length <= 1){
//             tag.classList.add('active-tag')
//             checkInput.checked = true
//             // tag.className = "active-tag"
//         }else{
//             tag.classList.remove('active-tag')
//             checkInput.checked = false
//         }
//     })
// })
