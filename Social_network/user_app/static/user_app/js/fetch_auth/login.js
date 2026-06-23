
const formLogin = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

function ErrorPop() {
    errorMessage.classList.remove('hidden');
    errorMessage.textContent = 'Неправильна електронна пошта або пароль';
}

if (formLogin) {
    formLogin.addEventListener('submit', (event) => {
        event.preventDefault();

        if (errorMessage) {
            errorMessage.classList.add('hidden');
        }

        const url = formLogin.getAttribute('action');
        const formData = new FormData(formLogin);
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
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
            window.location.href = '/';
        })
        .catch((data) => {
            if (data.errors || data.message){
                console.log(data.errors);
                ErrorPop();
            }
        });
    });
}