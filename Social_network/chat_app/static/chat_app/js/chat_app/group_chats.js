const csrfToken = document.querySelector('meta[name="csrf-token"]').content

const modalShadow = document.querySelector("#welcome-shadow")
const step1Modal = document.querySelector("#first-modal-create") || document.querySelector("#first-modal-creat")
const step2Modal = document.querySelector("#finish-create-modal")
const btnCreateChat = document.querySelector(".create-chat")
const closeCrosses = document.querySelectorAll("#close-modals, #close-modals-cancel, #cancel-group-modal")

const groupUserCheckboxes = document.querySelectorAll(".group-user-checkbox")
const selectedCount = document.querySelector("#selected-count")
const selectedUsersList = document.querySelector("#selected-users-list")
const groupNameInput = document.querySelector("#group-name")

const nextGroupStepBtn = document.querySelector("#next-group-step")
const backGroupStepBtn = document.querySelector("#back-group-step")
const submitCreateGroupBtn = document.querySelector("#create-group")

function closeAllModals() {
    if (modalShadow) modalShadow.classList.add("hidden")
    if (step1Modal) step1Modal.classList.add("hidden")
    if (step2Modal) step2Modal.classList.add("hidden")
    
    if (groupNameInput) groupNameInput.value = ""
    groupUserCheckboxes.forEach(cb => cb.checked = false)
    if (selectedCount) selectedCount.textContent = "0"
    if (selectedUsersList) selectedUsersList.innerHTML = ""
}

if (btnCreateChat) {
    btnCreateChat.addEventListener('click', () => {
        if (modalShadow) modalShadow.classList.remove("hidden")
        if (step1Modal) step1Modal.classList.remove("hidden")
        if (step2Modal) step2Modal.classList.add("hidden")
    })
}

function updateSelectedCount() {
  const count = document.querySelectorAll(".group-user-checkbox:checked").length
  selectedCount.textContent = count;
}

function renderSelectedUsers() {
  selectedUsersList.innerHTML = "";
  groupUserCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
        const userDiv = document.createElement("div")

        const avatarPath = "/static/chat_app/images/alert_conteiner/example-message.svg"
        const binPath = "/static/chat_app/images/alert_conteiner/bin.svg"

        userDiv.className = "member"
        userDiv.innerHTML = `
            <div class="user-info">
                <img src="${avatarPath}" alt="avatar-icon">
                <p class="name">${checkbox.dataset.userName}</p>
            </div>

            <img src="${binPath}" alt="" class="bin">
        `

        selectedUsersList.appendChild(userDiv);
    }
  });
}

closeCrosses.forEach(cross => {
    cross.addEventListener('click', closeAllModals)
})

groupUserCheckboxes.forEach(cb => {
    cb.addEventListener('change', () => {
        updateSelectedCount()
    })
})

if (nextGroupStepBtn) {
    nextGroupStepBtn.addEventListener('click', () => {
        if (selectedUsersList) selectedUsersList.innerHTML = ""
        document.querySelectorAll(".group-user-checkbox:checked").forEach(cb => {
            renderSelectedUsers()            
        })

        if (step1Modal) step1Modal.classList.add("hidden")
        if (step2Modal) step2Modal.classList.remove("hidden")
    })
}

if (backGroupStepBtn) {
    backGroupStepBtn.addEventListener('click', () => {
        if (step2Modal) step2Modal.classList.add("hidden")
        if (step1Modal) step1Modal.classList.remove("hidden")
    })
}

if (submitCreateGroupBtn) {
    submitCreateGroupBtn.addEventListener('click', async () => {
        const name = groupNameInput.value.trim()

        const formData = new FormData()
        formData.append('name', name)
        
        document.querySelectorAll(".group-user-checkbox:checked").forEach(checkboxe => {
            formData.append('users', checkboxe.value)
        })

        const response = await fetch('/chat/create_group/', { 
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData
        })
        const data = await response.json()

        if (data.success) {
            closeAllModals()
            insertGroupChatCard(data.chat_id, data.name)
            openChatById(data.chat_id, data.name)
            
        }
        
    })
}

function insertGroupChatCard(chatId, chatName) {
    const groupListContainer = document.querySelector('.group-cont .message-list')
    if (!groupListContainer) return

    const emptyText = groupListContainer.querySelector('p:not(.nickname-card):not(.card-time)')
    
    if (emptyText && emptyText.textContent.includes("немає")) {
        emptyText.remove()
    }

    const now = new Date()
    const timeString = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
    const avatarSrc = "/static/chat_app/images/alert_conteiner/group-avatar.svg"
    
    const cardHTML = `
        <div class="block-card" data-chat-id="${chatId}" data-chat-title="${chatName}">
            <img src="${avatarSrc}" alt="avatar-icon">

            <div class="text-data">
                <div class="top-data">
                    <p class="nickname-card">${chatName}</p>
                    <p class="card-time">${timeString}</p>
                </div>

                <div class="bottom-data">
                    <p>Нова група створена</p>
                </div>
            </div>
        </div>
    `
    
    groupListContainer.insertAdjacentHTML('afterbegin', cardHTML)
}