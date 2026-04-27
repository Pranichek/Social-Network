const form = document.getElementById('form-registration');


if (form) {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const url = form.getAttribute('action');
        const formData = new FormData(form);
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        
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
            console.log("Користувач був успішно створений!");
        })
        .catch((data) => {
            if (data.errors){
                console.log(data.errors);
            }
        })
    });
}