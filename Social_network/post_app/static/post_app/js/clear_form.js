import { clearImagePreviews } from "./show_images.js"

export function clearFields() {
    const allFields = document.querySelectorAll('#input-form');

    allFields.forEach(inputField => {
        inputField.value = '';
    });

    clearImagePreviews();

    const fileField = document.querySelector("#id_images");

    if (fileField) {
        fileField.value = '';
    }

    const linkBlocks = document.querySelectorAll('.input-block');
    if (linkBlocks.length > 0) {
        const firstLink = linkBlocks[0].querySelector('.input-link');
        if (firstLink) firstLink.value = '';

        for (let index = linkBlocks.length - 1; index >= 1; index--) {
            linkBlocks[index].remove();
        }
    }

    const divCheckBoxes = document.querySelector('.tags-container');
    if (divCheckBoxes) {
        const allCheckBoxes = divCheckBoxes.querySelectorAll('input[type="checkbox"]');
        allCheckBoxes.forEach(checkbox => {
            checkbox.checked = false; 
        });
    }
    const customTagsDiv = document.getElementById('custom-tags');
}