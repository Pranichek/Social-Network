const buttons = document.querySelectorAll('#button-card')

async function friendShipStatus(id, status){
    const response = await fetch(`/settings/friends/change_status/${status}/?id=${id}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    
    if (response.ok) {
        return await response.json()
    }
    return { success: false }
}


buttons.forEach(button => {
    button.addEventListener('click',async () => {
        const idPerson = button.value
        let status
        
        if (button.classList.contains('accepted-btn')){
            status = 'accepted'
        }
        else if (button.classList.contains('add-btn')){
            status = 'add'
        }
        
        const data = await friendShipStatus(idPerson, status)
        
        if (data && data.success) {
            button.closest('.person-card').remove()
            
            if (status == 'accepted' && data.html) {                
                const friendsContainer = document.getElementById('cards-friends')
                
                if (friendsContainer) {
                    friendsContainer.insertAdjacentHTML('afterbegin', data.html)
                }
            }
        }
    })
})

