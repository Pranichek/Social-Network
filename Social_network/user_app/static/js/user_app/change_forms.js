const createUser = document.querySelector('.create-user')
const sectionRegister = document.querySelector('.section-register')
const sectionLogin = document.querySelector('.section-login')
const sectionConfirmEmail = document.querySelector('.section-confirm')
const back = document.querySelector('#back')
const ButtonLogin = document.querySelectorAll('#ButtonLogin')
const ButtonRegister = document.querySelectorAll('#ButtonRegister')
let checkForm = 'register'


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
        if (checkForm != 'register'){
            sectionLogin.classList.toggle('hidden')
            sectionRegister.classList.toggle('hidden')
            checkForm = 'register'
        }
    })
})

ButtonLogin.forEach(button => {
    button.addEventListener('click', () => {
        if (checkForm != 'login'){
            sectionLogin.classList.toggle('hidden')
            sectionRegister.classList.toggle('hidden')
            checkForm = 'login'
        }
    
    })
})