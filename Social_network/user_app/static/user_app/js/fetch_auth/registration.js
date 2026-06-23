const form = document.getElementById('form-registration');
const sectionRegister = document.querySelector('.section-register');
const sectionLogin = document.querySelector('.section-login');
const sectionConfirmEmail = document.querySelector('.section-confirm');

if (form) {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const url = form.getAttribute('action');
        const formData = new FormData(form);
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const submitBtn = document.getElementById('create-account');

        if (submitBtn) {
            submitBtn.disabled = true
        }
        

        document.querySelectorAll('.fetch-error').forEach(el => el.remove());

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        }).then(async (response) => {
            const data = await response.json();

            if (!response.ok){
                throw data; 
            }
            
            return data;  
        })
        .then((data) => {
            sectionRegister.classList.toggle('hidden')
            sectionConfirmEmail.classList.toggle('hidden')
            imageLaptop.style.display = 'none'
        })
        .catch((errorData) => {
            document.querySelectorAll('.fetch-error').forEach(el => el.remove());

            if (submitBtn) {submitBtn.disabled = false}

            const errors = errorData.errors ? errorData.errors : errorData;

            if (errors) {
                for (const[fieldName, errorMessageData] of Object.entries(errors)) {
                    console.log(fieldName)
                    
                    let inputField = form.querySelector(`[name="${fieldName}"]`);

                    if (fieldName === '__all__') {
                        inputField = form.querySelector('[name="confirm_password"]');
                    }

                    let errorText = "";
                    if (Array.isArray(errorMessageData)) {
                        let firstError = errorMessageData[0];
                        errorText = firstError.message || firstError; 
                    } else {
                        errorText = errorMessageData;
                    }

                    const errorDiv = document.createElement('p');
                    errorDiv.className = 'fetch-error'; 
                    errorDiv.textContent = errorText;

                    if (inputField) {
                        const wrapper = inputField.closest('.password-wrapper');
                        
                        if (wrapper) {
                            wrapper.insertAdjacentElement('afterend', errorDiv);
                        } else {
                            inputField.insertAdjacentElement('afterend', errorDiv);
                        }
                    } else {
                        if (submitBtn) {
                            submitBtn.insertAdjacentElement('beforebegin', errorDiv);
                        } else {
                            form.appendChild(errorDiv);
                        }
                    }
                }
            }
        });
    });
}