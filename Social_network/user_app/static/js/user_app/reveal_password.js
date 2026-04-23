const passwordInputs = document.querySelectorAll('#password-input')

passwordInputs.forEach(input => {
    const eyeIcon = input.parentNode.querySelector('#eye-button')

    eyeIcon.addEventListener('click',()=>{
        const inputField = eyeIcon.parentNode.querySelector('#password-input')
        const eyeImg = eyeIcon.querySelector('#eye-img')
        

        if(inputField.type === 'password'){
            inputField.type = 'text'
            eyeImg.src = '/static/images/fields_images/open_eye.svg'
        }
        else{
            inputField.type = 'password'
            eyeImg.src = '/static/images/fields_images/closed_eye.svg'
        }
    })
})
