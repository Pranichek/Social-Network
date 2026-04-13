const allConsts = document.querySelectorAll('.link-page')


allConsts.forEach(cont => {
    cont.addEventListener('click', () => {
        const link = cont.querySelector('a').href
        location.replace(link)
        // link.click()
    })
})