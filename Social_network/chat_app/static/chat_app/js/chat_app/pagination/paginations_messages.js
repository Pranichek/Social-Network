let currentPageActiveChats = 2;
let isLoadingActiveChats = false;
let preloadedDataChats = null;

const sentielChats = document.getElementById("active-chats-sentinel");
const scrollContainerChats = document.getElementById("message-block-cards");

async function getDataChats() {
    const response = await fetch(
      `/chat/message_block/?page=${currentPageActiveChats}`,
      {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      },
    );
    const data = await response.json();
    return data;
}

async function loadPreDataChats() {
    const data = await getDataChats();
    preloadedDataChats = data; 
    currentPageActiveChats++; 
}

document.addEventListener('DOMContentLoaded', () => {
    loadPreDataChats();
});

const observerChats = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && !isLoadingActiveChats) {
        isLoadingActiveChats = true;
    
        if (!preloadedDataChats) {
            await loadPreDataChats();
        }

        if (preloadedDataChats) { 
            if (preloadedDataChats.html) {
                sentielChats.insertAdjacentHTML("beforebegin", preloadedDataChats.html);
                window.reloadDict()
                console.log(currentId)
                window.recheckCard(currentId)
                window.reapplyUnreadData()
            }

            if (!preloadedDataChats.has_next) {
                observerChats.disconnect();
                sentielChats.remove();
            } else {
                preloadedDataChats = null; 
                loadPreDataChats(); 
            }
        }

        isLoadingActiveChats = false;
    }
}, {
    root: scrollContainerChats,
    rootMargin: "100px"        
});

if (sentielChats && scrollContainerChats) {
    observerChats.observe(sentielChats);
} 