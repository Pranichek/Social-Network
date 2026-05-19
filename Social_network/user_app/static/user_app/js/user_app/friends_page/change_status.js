const buttons = document.querySelectorAll('#button-card');

async function friendShipStatus(id, status){
    const response = await fetch(`/settings/friends/change_status/${status}/?id=${id}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
}


buttons.forEach(button => {
    button.addEventListener('click',async () => {
        const idPerson = button.value
        let status;
        
        if (button.classList.contains('accepted-btn')){
            status = 'accepted'
        }
        else if (button.classList.contains('add-btn')){
            status = 'add'
        }
        
        await friendShipStatus(idPerson, status)
    })
})

