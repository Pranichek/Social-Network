let currentPageContacts = 2;
let isLoadingContacts = false;

let preloadedData = null;


const contactList = document.querySelector("#all-contacts");
const sentinel = document.getElementById("contact-load-sentinel");

async function getData() {
    const response = await fetch(
      `/chat/contacts/?page=${currentPageContacts}`,
      {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      },
    );
    const data = await response.json();

    return data;
}


async function loadPreData() {
    const data = await getData();
    preloadedData = data; 
    currentPageContacts++; 
}

document.addEventListener('DOMContentLoaded', () => {
    loadPreData();
});

const observerContact = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && isLoadingContacts == false) {
        isLoadingContacts = true;
    
        if (preloadedData) { 
            if (preloadedData.html) {
                sentinel.insertAdjacentHTML("beforebegin", preloadedData.html);
                window.reloadDict()
            }

            if (!preloadedData.has_next) {
                observerContact.disconnect();
                sentinel.remove();
            } else {
                // без await, щоб завантажували дані у фоновому режимі
                loadPreData(); 
            }
        }

        isLoadingContacts = false;
    }
}, {rootMargin: "200px"});

if (sentinel) {
    observerContact.observe(sentinel);
}

