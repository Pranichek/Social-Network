const buttons = document.querySelectorAll('#button-card')
console.log(buttons)

async function friendShipStatus(id, status) {
    try {
        const response = await fetch(`/settings/friends/change_status/${status}/?id=${id}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        
        if (response.ok) {
            return await response.json()
        }
        
        return { success: false }
    } catch (error) {
        console.error(error)
        return { success: false }
    }
}

window.friendShipStatus = friendShipStatus

// buttons.forEach(button => {
//     console.log(67)
//     button.addEventListener('click', (e) => {
//         let status
        
//         if (button.classList.contains('accepted-btn')) {
//             status = 'accepted'
//         } else if (button.classList.contains('add-btn')) {
//             console.log(83)
//             status = 'add'
//         } else if (button.classList.contains('decline-btn')) {
//             console.log(23)
//             status = 'delete'
//         } else {
//             console.log(99) 
//             return
//         }        
        
//     })
// })