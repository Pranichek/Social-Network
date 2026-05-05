const allFields = document.querySelectorAll('#input-form')

export function clearFields(){
    const links = document.querySelectorAll('#input-link')
    const fileField = document.querySelector("#id_images")
    const divCheckBoxes = document.querySelector('#id_tags')
    const allCheckBoxes = divCheckBoxes.querySelectorAll('input')

    

    allFields.forEach(inputField => {
        inputField.value = ''
    })

    fileField.value = ''

    links[0].value = ''
    if (links.length > 1){
        for (let index = links.length - 1; index >= 1; index--){
            links[index].remove()
            links.pop()
        }
    }

    allCheckBoxes.forEach(checkbox => {
        checkbox.checked = false
    })
}