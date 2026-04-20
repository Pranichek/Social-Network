const createUser = document.querySelector('.create-user')
const sectionRegister = document.querySelector('.section-register')
const sectionLogin = document.querySelector('.section-login')
const sectionConfirmEmail = document.querySelector('.section-confirm')
const back = document.querySelector('#back')



createUser.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
})

back.addEventListener('click', () => {
    sectionRegister.classList.toggle('hidden')
    sectionConfirmEmail.classList.toggle('hidden')
})
