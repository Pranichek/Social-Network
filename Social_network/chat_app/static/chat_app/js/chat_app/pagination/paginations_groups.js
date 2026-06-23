let currentPageGroupChats = 2;
let isLoadingGroupChats = false;
let preloadedDataGroupChats = null;


const sentinelGroupChats = document.getElementById("group-sentinel");
const scrollContainerGroupChats = document.getElementById("group-block-cards");

async function getGroupChatsData() {
    const response = await fetch(
      `/chat/group_block/?page=${currentPageGroupChats}`,
      {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      },
    );
    const data = await response.json();
    return data;
}

async function loadPreDataGroupChats() {
    const data = await getGroupChatsData();
    preloadedDataGroupChats = data; 
    currentPageGroupChats++; 
}

document.addEventListener('DOMContentLoaded', () => {
    if (sentinelGroupChats) {
        loadPreDataGroupChats();
    }
});

const observerGroupChats = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && !isLoadingGroupChats) {
        isLoadingGroupChats = true;
    
        if (!preloadedDataGroupChats) {
            await loadPreDataGroupChats();
        }

        if (preloadedDataGroupChats) { 
            if (preloadedDataGroupChats.html) {
                sentinelGroupChats.insertAdjacentHTML("beforebegin", preloadedDataGroupChats.html);
                window.reloadDict()
                window.reapplyUnreadData()
            }

            if (!preloadedDataGroupChats.has_next) {
                observerGroupChats.disconnect();
                sentinelGroupChats.remove();
            } else {
                preloadedDataGroupChats = null; 
                loadPreDataGroupChats(); 
            }
        }

        isLoadingGroupChats = false;
    }
}, {
    root: scrollContainerGroupChats,
    rootMargin: "100px"        
});

if (sentinelGroupChats && scrollContainerGroupChats) {
    observerGroupChats.observe(sentinelGroupChats);
} 