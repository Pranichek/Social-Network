const buttons = document.querySelectorAll('#button-card'); 

async function friendShipStatus(id, status) {
    const response = await fetch(`/settings/friends/change_status/${status}/?id=${id}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
    const data = await response.json();

    if (status === 'add') {
        const friendsSection = document.getElementById('friends-section');
        if (friendsSection && data.html) {
            friendsSection.insertAdjacentHTML('beforeend', data.html);
        }
    }
    
    return data;  
}


buttons.forEach(button => {
    button.addEventListener('click', async () => {
        const idPerson = button.value;
        const card = button.closest('.person-card') || button.parentElement; 

        let status;
        if (button.classList.contains('accepted-btn')) {
            status = 'accepted';
        } else if (button.classList.contains('add-btn')) {
            status = 'add';
        }
        
        await friendShipStatus(idPerson, status);

        if (card) {
            card.remove(); 
        }
    });
});