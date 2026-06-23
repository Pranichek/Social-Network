const createUser = document.querySelector('.create-user')
const sectionRegister = document.querySelector('.section-register')
const sectionLogin = document.querySelector('.section-login')
const sectionConfirmEmail = document.querySelector('.section-confirm')
const back = document.querySelector('#back')
const ButtonLogin= document.querySelectorAll('#ButtonLogin')
const ButtonRegister = document.querySelectorAll('#ButtonRegister')


createUser.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
})

back.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
})

ButtonRegister.forEach(button => {
    button.addEventListener('click', () => {
        sectionLogin.classList.toggle('hidden')
        sectionRegister.classList.toggle('hidden')
    })
})

ButtonLogin.forEach(button => {
    button.addEventListener('click', () => {
        sectionLogin.classList.toggle('hidden')
        sectionRegister.classList.toggle('hidden')
    })
})