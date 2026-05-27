const modalShadow = document.querySelector("#welcome-shadow")
const newGroup = document.querySelector(".modal-form-create")
const newGroupFinish = document.querySelector("#finish-create")
const btnCreate = document.querySelector(".create-chat")
const massiveModals = [newGroup, newGroupFinish]

const closeCrosses = document.querySelectorAll("#close-modals")

const changeModals = document.querySelectorAll(".change-modal")

btnCreate.addEventListener('click', () => {
    modalShadow.classList.toggle("hidden")
    newGroup.classList.toggle("hidden")
})

closeCrosses.forEach((cross) => {
    cross.addEventListener('click', () => {
        modalShadow.classList.toggle("hidden")
        massiveModals.forEach(modal => {
            if (!modal.classList.contains('hidden')){
                modal.classList.toggle("hidden")
            }
        })
    })
})

changeModals.forEach(button => {
    button.addEventListener("click", () => {
        massiveModals.forEach(modal => {
        modal.classList.toggle("hidden")
    })
    })
})
