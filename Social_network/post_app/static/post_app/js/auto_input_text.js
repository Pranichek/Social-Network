const inputField = document.getElementById('input-content')
const textAreaField = document.querySelector(".content-area")


inputField.addEventListener('input', () => {
    textAreaField.value = inputField.value
})


textAreaField.addEventListener('input', () => {
    inputField.value = textAreaField.value
})
