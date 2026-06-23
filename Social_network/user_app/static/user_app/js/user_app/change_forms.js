import { clearFields } from './clear_forms.js'

const sectionRegister = document.querySelector('.section-register')
const sectionLogin = document.querySelector('.section-login')
const sectionConfirmEmail = document.querySelector('.section-confirm')
const back = document.querySelector('#back')
const ButtonLogin = document.querySelectorAll('#ButtonLogin')
const ButtonRegister = document.querySelectorAll('#ButtonRegister')
const imageLaptop = document.querySelector('.laptop-image')
let checkForm = 'register'


back.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
    imageLaptop.style.display = 'block'
    clearFields()
})

ButtonRegister.forEach(button => {
    button.addEventListener('click', () => {
        if (checkForm != 'register'){
            sectionLogin.classList.toggle('hidden')
            sectionRegister.classList.toggle('hidden')
            checkForm = 'register'
            clearFields()
        }
    })
})

ButtonLogin.forEach(button => {
    button.addEventListener('click', () => {
        if (checkForm != 'login'){
            sectionLogin.classList.toggle('hidden')
            sectionRegister.classList.toggle('hidden')
            checkForm = 'login'
            clearFields()
        }
    
    })
})