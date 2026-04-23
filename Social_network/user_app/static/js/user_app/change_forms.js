const createUser = document.querySelector('.create-user')
const sectionRegister = document.querySelector('.section-register')
const sectionLogin = document.querySelector('.section-login')
const sectionConfirmEmail = document.querySelector('.section-confirm')
const back = document.querySelector('#back')
const ButtonLogin = document.querySelectorAll('#ButtonLogin')
const ButtonRegister = document.querySelectorAll('#ButtonRegister')
const imageLaptop = document.querySelector('.laptop-image')
let checkForm = 'register'


createUser.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
    imageLaptop.style.display = 'none'
})

back.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
    imageLaptop.style.display = 'block'
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