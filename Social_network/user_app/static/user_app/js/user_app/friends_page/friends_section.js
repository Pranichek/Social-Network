
const mainBlock = document.getElementById('friends-main')
const sectionBlock = document.getElementById('section')
const sectionTitle = document.getElementById('section-title')
const sectionList = document.getElementById('section-list')
const loadSentinel = document.getElementById('loader-line')
const backMain = document.getElementById('back-main')
const sectionButtons = document.querySelectorAll('[data-section-link]')

const sectionTitles = {
    requests: 'Запити',
    recommendations: 'Рекомендації',
    friends: 'Всі друзі'
}

let currentSection = ''
let currentPage = 1
let hasNextPage = true
let isLoading = false


async function loadSectionPage(section, page) {
    isLoading = true
    const response = await fetch(`/settings/friends/${section}/?page=${page}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
    sectionList.insertAdjacentHTML('beforeend', data.html)
    hasNextPage = data.has_next_page
    isLoading = false
}

async function openSection(section) {
    currentSection = section
    currentPage = 1
    hasNextPage = false
    sectionTitle.textContent = sectionTitles[section]
    sectionList.innerHTML = ''
    mainBlock.style.display = 'none'
    sectionBlock.style.display = 'flex'
    await loadSectionPage(section, currentPage)
}


function OpenMain() {
    sectionBlock.style.display = 'none'
    sectionList.innerHTML = ''
    currentSection = ''
    hasNextPage = false
    mainBlock.style.display = 'flex'

}
const observer = new IntersectionObserver(
    async (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isLoading) {
            currentPage++
            await loadSectionPage(currentSection, currentPage)
        }
    }, {
        rootMargin: '200px',
    }
)


observer.observe(loadSentinel)


backMain.addEventListener('click', OpenMain)

sectionButtons.forEach(button => {
    button.addEventListener('click',async () => {

        if (button.classList.contains('main-link')){
            OpenMain()
        }
        else {
            await openSection(button.dataset.sectionLink)
        }
        

        sectionButtons.forEach(btn => {
            if (btn.classList.contains('bottom-line')){
                btn.classList.remove('bottom-line')
            }
            
            // Якщо датасет тегу з бокового меню  такий же самий, як у кнопки на яку натиснули
            // то в такому випадку, ми можемо додати саме до тегу з бокового меню клас bottom-line
            if (btn.dataset.sectionLink == button.dataset.sectionLink){
                // робимо перевірку, щоб не додати клас до кнопку на секції
                if (!btn.classList.contains('section-button')){
                    btn.classList.add('bottom-line')
                }
            }

        })

        // button.classList.add('bottom-line')
    })
})