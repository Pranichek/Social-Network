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
    
    if (response.ok) {
        const data = await response.json()
        sectionList.insertAdjacentHTML('beforeend', data.html)
        hasNextPage = data.has_next_page
    }
    
    isLoading = false
}

async function openSection(section) {
    if (currentSection == section) return

    currentSection = section
    currentPage = 1
    hasNextPage = false
    sectionTitle.textContent = sectionTitles[section]
    sectionList.innerHTML = ''
    
    mainBlock.classList.add("hidden")
    sectionBlock.classList.remove("hidden")

    mainBlock.style.display = ''
    sectionBlock.style.display = ''

    await loadSectionPage(section, currentPage)
}

function OpenMain() {
    sectionBlock.classList.add("hidden")
    mainBlock.classList.remove("hidden")
    
    mainBlock.style.display = ''
    sectionBlock.style.display = ''
    
    sectionList.innerHTML = ''
    currentSection = ''
    hasNextPage = false
}

window.OpenMain = OpenMain

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

if (loadSentinel) observer.observe(loadSentinel)

if (backMain) backMain.addEventListener('click', OpenMain)

sectionButtons.forEach(button => {
    button.addEventListener('click', async () => {

        if (button.classList.contains('main-link')) {
            OpenMain()

            document.querySelectorAll(".section-button").forEach(selectBtn => {
                selectBtn.style.display = 'flex'
            })
        }
        else {
            await openSection(button.dataset.sectionLink)

            document.querySelectorAll(".section-button").forEach(selectBtn => {
                selectBtn.style.display = 'none'
            })
        }

        
        sectionButtons.forEach(btn => {
            if (btn.classList.contains('bottom-line')) btn.classList.remove('bottom-line')
            
            if (btn.dataset.sectionLink == button.dataset.sectionLink) {
                if (!btn.classList.contains('section-button')) btn.classList.add('bottom-line')
            }
        })
    })
})