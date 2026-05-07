const inputField = document.getElementById('input-content')
const textAreaField = document.querySelector(".content-area")
console.log(textAreaField)


inputField.addEventListener('input', () => {
    textAreaField.value = inputField.value
})


textAreaField.addEventListener('input', () => {
    inputField.value = textAreaField.value
})
