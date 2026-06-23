const currentPath = window.location.pathname
const linkContainers = document.querySelectorAll('.link-page')

linkContainers.forEach(container => {
    const link = container.querySelector('a')
    
    if (link) {
        const linkPath = link.getAttribute('href')


        if (linkPath === '/' && currentPath === '/') {
            container.classList.add('active')
        } else if (linkPath !== '/' && currentPath.startsWith(linkPath)) {
            container.classList.add('active')
        } else {
            container.classList.remove('active')
        }
    }
})
