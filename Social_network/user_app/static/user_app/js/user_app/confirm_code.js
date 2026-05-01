const sectionConfirmEmail = document.querySelector('.section-confirm')
const codeInputs = document.querySelectorAll('.confirm-number')


codeInputs.forEach((input, index) => {
    
    input.addEventListener('input', () => {
        if (input.value.length > 1) {
            input.value = input.value.slice(0, 1);
        }

        if (input.value.length === 1 && codeInputs[index + 1]) {
            codeInputs[index + 1].disabled = false 
            codeInputs[index + 1].focus()          
        }
    })
    
    input.addEventListener('keydown', (event) => {
        if (event.key === 'Backspace' && input.value === '' && codeInputs[index - 1]) {
            codeInputs[index - 1].focus() 
        }
    })
})