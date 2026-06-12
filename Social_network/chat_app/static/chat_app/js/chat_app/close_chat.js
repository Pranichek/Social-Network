const closeChat = document.getElementById('close-chat');

const headerChats = document.getElementById('header-chat');
const mainText = document.getElementById('main-text');
const bottomPart = document.getElementById('chat-window');
const allElements = [headerChats, mainText, bottomPart];

const mainBlock = document.querySelector('.texting-box');


function showMainPrevview(){
    allElements.forEach((element) => {
        element.classList.toggle('hidden')
    });
    if (mainBlock.classList.contains('show-chat')){
        mainBlock.classList.remove('show-chat')
    }
}

window.showMainPrevview = showMainPrevview

closeChat.addEventListener('click', (event) => {

    showMainPrevview()
})

document.addEventListener('DOMContentLoaded', () => {
    const userCheckboxes = document.querySelectorAll('.group-user-checkbox');
    const nextBtn = document.getElementById('next-group-step');
    const selectedCountSpan = document.getElementById('selected-count');

    function checkUsersCount() {
        const checkedBoxes = document.querySelectorAll('.group-user-checkbox:checked');
        const selectedCount = checkedBoxes.length;

        if (selectedCountSpan) {
            selectedCountSpan.textContent = selectedCount;
        }

        if (selectedCount < 2) {
            nextBtn.disabled = true;
            nextBtn.style.opacity = '0.5';
            nextBtn.style.cursor = 'not-allowed';
        } else {
            nextBtn.disabled = false;
            nextBtn.style.opacity = '1';
            nextBtn.style.cursor = 'pointer';
        }
    }

    userCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', checkUsersCount);
    });

    if (nextBtn) {
        checkUsersCount();
    }
});