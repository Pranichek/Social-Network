let activeChatId = null;
let currentPage = 1;
let hasNext = false;
let isLoading = false;
let observer = null;

const messages = document.querySelector("#messeages");

function padDateNumber(number){
  return String(number).padStart(2, '0');
}

function formatMessageTime(createdAt){
  const date = new Date(createdAt);
  return `${padDateNumber(date.getHours())}:${padDateNumber(date.getMinutes())}`;
}

const months = [
  "Січень",
  "Лютий",
  "Березень",
  "Квітень",
  "Травень",
  "Червень",
  "Липень",
  "Серпень",
  "Вересень",
  "Жовтень",
  "Листопад",
  "Грудень"
];

function formatMessageDate(createdAt){
  const date = new Date(createdAt);
  const monthIndex = date.getMonth();
  const nameMonth = months[monthIndex];

  
  return `${padDateNumber(date.getDate())} ${nameMonth} ${padDateNumber(date.getFullYear())}`;
}

function renderDateSeparator(dateText){
  const separator = document.createElement('div');

  const outlineText = document.createElement('div');
  outlineText.className = 'outline-text';

  const textSeparator = document.createElement("p");
  textSeparator.textContent = dateText

  outlineText.appendChild(textSeparator);
  
  separator.appendChild(outlineText);
  separator.classList.add('message-separator');

  return separator;
}

function updateSeparators(){
  const allSeparators = document.querySelectorAll('.message-separator');
  allSeparators.forEach((separator) => {
    separator.remove();
  }) 

  let previousDate = '';
  const allMessages = document.querySelectorAll('.message');
  allMessages.forEach((message) => {
    const messageDate = message.dataset.messageDate;
    if (messageDate !== previousDate){
      message.before(renderDateSeparator(messageDate));
      previousDate = messageDate;
    }
  })
}

window.updateSeparators = updateSeparators;


function renderMessage(data) {
  const messageDiv = document.createElement("div");
  const isMe = data.is_current_user;
  console.log(isMe)
  const msgClass = isMe ? "message" : "message other_user";
  const outlineClass = isMe ? "message-outline" : "other-message-outline";
  const checkReadIconPath = '/static/chat_app/images/chat_images/check_read.svg';

  messageDiv.className = msgClass;
  messageDiv.dataset.messageDate = formatMessageDate(data.created_at)

  if (window.hasMessageImages(data)){
    messageDiv.appendChild(window.renderMessageImage(data.images));
  }

  messageDiv.insertAdjacentHTML('beforeend', `
    <div class="${outlineClass}">
        <div class="msg-text">
            <p>${data.message_text ? data.message_text : ""}</p>
        </div>
        <div class="data-message">
            <p>${formatMessageTime(data.created_at)}</p>
            <img src="${checkReadIconPath}" alt="check_read">
        </div>
    </div>
  `);

  return messageDiv;
}

function resetMessages(chatId) {
  activeChatId = chatId;
  currentPage = 1;
  hasNext = true;
  isLoading = false;
  if (observer) observer.disconnect();
  messages.innerHTML = "";
  const sentinel = document.createElement("div");
  sentinel.id = "chat-load-sentinel";
  messages.prepend(sentinel);
}

async function loadMessages(prepend = false) {
  if (isLoading || !hasNext) return;
  isLoading = true;
  const oldHeight = messages.scrollHeight;

  const response = await fetch(
    `/chat/${activeChatId}/messages/?page=${currentPage}`,
    {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    }
  );
  const data = await response.json();

  if (data.success) {
    const fragment = document.createDocumentFragment();
    data.messages.forEach((message) =>
      fragment.appendChild(renderMessage(message))
    );

    const sentinel = document.querySelector("#chat-load-sentinel");
    if (prepend) {
      sentinel.after(fragment);
    } else {
      messages.appendChild(fragment);
    }

    hasNext = data.has_next;
    currentPage++;

    if (prepend) {
      messages.scrollTop = messages.scrollHeight - oldHeight;
    } else {
      messages.scrollTop = messages.scrollHeight;
    }
  }

  if (!hasNext && observer) observer.disconnect();
  isLoading = false;
}

function startObserver() {
  const sentinel = document.querySelector("#chat-load-sentinel");
  observer = new IntersectionObserver(
    async (entries) => {
      if (entries[0].isIntersecting && isLoading == false) {
        await loadMessages(true);
        updateSeparators();
      }
    },
    { root: messages, rootMargin: "20px" }
  );
  if (sentinel) observer.observe(sentinel);
}