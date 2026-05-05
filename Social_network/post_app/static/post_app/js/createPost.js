import { clearFields } from "./clear_form.js"

const linksDiv = document.querySelector("#links-list")
const customTagsDiv = document.getElementById('custom-tags')

document.querySelector("#add-link").addEventListener('click', () => {
    const input = document.createElement('input')
    input.type = 'url'
    input.name = 'links'
    input.placeholder = 'Додайте посилання'
    input.id = 'input-link'

    linksDiv.append(input)
})

document.querySelector('#add-custom-tag').addEventListener('click', () => {
    const input = document.createElement('input')
    input.type = 'text'
    input.name = 'custom_tags'
    input.placeholder = 'Додайте тег'
    input.className = 'input-custom-tag'
    customTagsDiv.append(input)

})

function getCSRFToken(){
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
}


document.getElementById('create-post').addEventListener('submit', function(event) {
    event.preventDefault()

    const form = event.target
    const formData = new FormData(form)

    fetch(form.action, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        body: formData,
    }).then(async (responce) => {
        const data = await responce.json()

        if (!responce.ok){
            throw data
        }

        return data
    }).then((data) => {
        console.log('Пост успішно створено')
        clearFields()
    }).catch((data) => {
        if (data.errors){
            console.log(data.errors)
        }
    })
})