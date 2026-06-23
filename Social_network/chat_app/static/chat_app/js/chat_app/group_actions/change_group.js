const csrfTokenGroup = document.querySelector('meta[name = "csrf-token"]').content;
const changeGroupForm = document.querySelector('.change-group-form');
const changeGroupChatId = document.querySelector('#change-group-chat-id');
const changeGroupName = document.querySelector('#change-group-name');
const changeGroupMemberList = document.querySelector('#change-group-member-list');
const modalShow = document.querySelector('#welcome-shadow');

let selectedMembers = new Map();

function openChangeGroupModal(chatId, chatName, chatMembers) {
    changeGroupChatId.value = chatId,
    changeGroupName.value = chatName,
    selectedMembers.clear();
    chatMembers.forEach((member) => {
        selectedMembers.set(member.id, member);
    })

    renderChangeGroupMembers();

    modalShadow.classList.remove('hidden');
    changeGroupChatId.classList.remove('hidden');
}

function renderChangeGroupMembers(){
    changeGroupMemberList.innerHTML = '';
    selectedMembers.forEach((member, userId) => {
        const card = document.createElement('div')
        card.classList.add('member-card')
        card.dataset.userId = userId
        card.innerHTML = `
            <div class = "circle-icon"><p>NG</p></div>
            <div class = "member-info">
                <p>${member.name}</p>
                <img src = "/static/chat_app/images/modals_chat/trash-icon.svg" class="remove-member-btn data-user-id=${userId}> 
            </div>
        `

        changeGroupMemberList.appendChild(card)
    })

    changeGroupMemberList.querySelectorAll('.remove-member-btn').forEach((button) => {
        button.addEventListener('click', () => {
            selectedMembers.delete(Number(button.dataset.userId))
            renderChangeGroupMembers()
        })
    })
}