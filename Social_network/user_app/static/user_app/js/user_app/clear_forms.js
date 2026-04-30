const sectionRegister = document.querySelector('.section-register')
const sectionLogin = document.querySelector('.section-login')
const sectionConfirmEmail = document.querySelector('.section-confirm')

export function clearFields(){
    let allSections = [sectionConfirmEmail, sectionLogin, sectionRegister]

    allSections.forEach(section => {
        let form = section.querySelector('form')
        let inputs = form.querySelectorAll('input')

        inputs.forEach(input => {
            input.value = null
        })
    })
}
