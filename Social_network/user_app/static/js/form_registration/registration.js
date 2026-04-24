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
                // 'Content-Type': 'application/json'
                // 'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })

        console.log(1)
    });
}