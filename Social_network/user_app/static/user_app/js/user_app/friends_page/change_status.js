const buttons = document.querySelectorAll('.button-card')

async function friendShipStatus(id, status) {
    try {
        const response = await fetch(`/settings/friends/change_status/${status}/?id=${id}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        
        if (response.ok) return await response.json()
        
        return { success: false }
    } catch (error) {
        console.error('Ошибка:', error)
        return { success: false }
    }
}

window.friendShipStatus = friendShipStatus

buttons.forEach(button => {
    button.addEventListener('click', async (e) => {
        e.stopPropagation() 

        const idPerson = button.value
        let status
        
        if (button.classList.contains('accepted-btn')) status = 'accepted'
        else if (button.classList.contains('add-btn')) status = 'add'
        else if (button.classList.contains('decline-btn')) status = 'delete'
        else return
        
        button.disabled = true
        
        const data = await friendShipStatus(idPerson, status)
        
        if (data && data.success) {
            const card = button.closest('.person-card')
            if (card) card.remove()
            
            if (status == 'accepted' && data.html) {                
                const friendsContainer = document.getElementById('cards-friends')
                if (friendsContainer) friendsContainer.insertAdjacentHTML('afterbegin', data.html)
            }
            
            if (status == 'delete' && data.html) {
                const recommendationsContainer = document.getElementById('cards-recommendations')
                
                if (recommendationsContainer) {
                    recommendationsContainer.insertAdjacentHTML('afterbegin', data.html)
                }
            }
        }
        
        button.disabled = false
    })
})