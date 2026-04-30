import { clearFields } from '../user_app/clear_forms.js'

const formConfirm = document.getElementById('confirm-form');

function returnCode(){
    const allInputs = document.querySelectorAll('.confirm-number');
    let code = ''

    allInputs.forEach(input => {
        code += String(input.value)
    })

    return code
}


if (formConfirm) {
    formConfirm.addEventListener('submit', (event) => {
        event.preventDefault();
        const url = formConfirm.getAttribute('action');
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        const code = returnCode();
        const formData = new FormData();
        formData.append('code', code); 
                
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        }).then(async (response) => {
            const data = await response.json()

            if (!response.ok){
                throw data;
            }
            
            return data  
        })
        .then((data) => {
            sectionConfirmEmail.classList.toggle('hidden')
            sectionLogin.classList.toggle('hidden')
            imageLaptop.style.display = 'block'
            clearFields()
        })
        .catch((data) => {
            if (data.errors){
                console.log(data.errors);
            }
        })
    });
}