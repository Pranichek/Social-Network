const createPost = document.getElementById('show-form')
const formPost = document.getElementById('create-post')
const closePost = document.getElementById('close-form')

createPost.addEventListener('click',() => {
    formPost.classList.remove('hidden')
})

closePost.addEventListener('click', () =>{
    formPost.classList.add('hidden')
})