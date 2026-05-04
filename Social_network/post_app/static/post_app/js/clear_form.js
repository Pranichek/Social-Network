const allFields = document.querySelectorAll('#input-form')


export function clearFields(){
    const links = document.querySelectorAll('#input-link')

    allFields.forEach(inputField => {
        inputField.value = ''
    })

    links[0].value = ''
    if (links.length > 1){
        for (let index = links.length - 1; index >= 1; index--){
            links[index].remove()
            links.pop()
        }
    }
}