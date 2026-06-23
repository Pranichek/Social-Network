const imageInput = document.getElementById('message-images');
const messageImageButton = document.getElementById('message-button');

function getSelectImages() {
    return Array.from(imageInput.files);
}

function hasSelectedImages(){
    return getSelectImages().length > 0;
}

function clearSelectedImages(){
    imageInput.value = '';
}

async function sendMessageWithImages(text){
    const formData = new FormData();
    formData.append('text', text);
    getSelectImages().forEach((image) => {
        formData.append('images', image);
    })

    const response = await fetch(`/chat/upload_images/${currentChatId}/`, {
        method : 'POST',
        headers : {'X-CSRFToken': csrfToken},
        body : formData,
    });
    return response.json();
}


messageImageButton.addEventListener('click', ()=>{
    imageInput.click();
})

window.hasSelectedImages = hasSelectedImages;
window.sendMessageWithImages = sendMessageWithImages;

function hasMessageImages(data){
    return Array.isArray(data.images) && data.images.length > 0;
}

function renderMessageImage(imageUrls) {
    const imgList = document.createElement('div');
    imgList.classList.add('message-images');

    imageUrls.forEach((item) => {
        const url = typeof item === 'string' ? item : item?.image
        if (!url) return

        const img = document.createElement('img');
        img.src = url;
        console.log(url, "dfkmvfdkl")
        imgList.appendChild(img);
    })
    return imgList;
}

window.hasMessageImages = hasMessageImages;
window.renderMessageImage = renderMessageImage;