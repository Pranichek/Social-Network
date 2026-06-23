const endForm = document.getElementById('end-register');
const welcomeMessage = document.getElementById('message');
const shadow = document.getElementById('welcome-shadow');

if (endForm) {
    endForm.addEventListener('submit', (event) => {
        event.preventDefault(); 

        const formData = new FormData(endForm);
        const url = endForm.getAttribute('action');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(async (response) => {
            const data = await response.json();
            if (!response.ok) throw data;
            return data;
        })
        .then((data) => {
            if (data.success) {
                welcomeMessage.classList.add('hidden');
                shadow.classList.add('hidden');                    
            }
        })
        .catch((errorData) => {
            if (errorData){
                console.error(errorData);
            }
        });
    });
}
