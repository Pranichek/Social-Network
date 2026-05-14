document.addEventListener('DOMContentLoaded', function() {

    const Links = document.querySelectorAll('.link-page');
    // let currentUrl = '/post/posts';

    let currentUrl = window.location.pathname.split('/')[1];
    console.log(currentUrl);

    // currentUrl = currentUrl.split('/')

    // window.onload = function() {
    if(currentUrl === ''){
        currentUrl = 'home';    
    }

    console.log(cur)
    Links.forEach(link=> {
        if (link.className.includes( currentUrl + '-link')){ {
            link.classList.add('active');
        }}else{
            link.classList.remove('active');
        }
    })
})
