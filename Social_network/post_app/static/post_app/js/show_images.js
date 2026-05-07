const fileInput = document.getElementById('id_images');
const previewContainer = document.getElementById('image-preview-container');

let selectedFiles = [];

fileInput.addEventListener('change', (event) => {
    const files = Array.from(event.target.files);    
    selectedFiles = selectedFiles.concat(files);
    
    updateFileInput();
    renderPreviews();
});

function renderPreviews() {
    previewContainer.innerHTML = '';

    selectedFiles.forEach((file, index) => {
        const imgUrl = URL.createObjectURL(file);

        const previewDiv = document.createElement('div');
        previewDiv.classList.add('preview-item');

        previewDiv.innerHTML = `
            <img src="${imgUrl}" class="preview-image" alt="preview">
            <div class="delete-btn" data-index="${index}">
                <img src="/static/post_app/images/posts_images/trash_icon.svg" alt="del">
            </div>
        `;
        previewContainer.appendChild(previewDiv);
    });

    document.querySelectorAll('.delete-btn').forEach(delBtn => {
        delBtn.addEventListener('click', function() {
            const indexToRemove = parseInt(this.getAttribute('data-index'));
            
            selectedFiles.splice(indexToRemove, 1);
            
            updateFileInput();
            renderPreviews();
        });
    });
}

function updateFileInput() {
    const dataTransfer = new DataTransfer();
    
    selectedFiles.forEach(file => {
        dataTransfer.items.add(file);
    });
    
    fileInput.files = dataTransfer.files;
}


export function clearImagePreviews() {
    selectedFiles = [];
    updateFileInput();  
    renderPreviews();  
}