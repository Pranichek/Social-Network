const linksDiv = document.querySelector("#links-list")

document.querySelector("#add-link").addEventListener('click', () => {
    const input = document.createElement('input')
    input.type = 'url'
    input.name = 'links'
    input.placeholder = 'Додайте посилання'

    linksDiv.append(input)
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
    }).catch((data) => {
        if (data.errors){
            console.log(data.errors)
        }
    })
})