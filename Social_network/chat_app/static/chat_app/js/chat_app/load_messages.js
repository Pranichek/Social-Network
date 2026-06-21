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

window.formatMessageTime = formatMessageTime

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


function renderMessage(data, username, isGroup) {
  const messageDiv = document.createElement("div");
  const isMe = data.is_current_user;
  const msgClass = isMe ? "message" : "message other_user";
  const outlineClass = isMe ? "message-outline" : "other-message-outline";
  const checkReadIconPath = '/static/chat_app/images/chat_images/check_read.svg';
  const hasImages = window.hasMessageImages(data);
  const hasText = data.message_text && data.message_text.trim() !== "";

  messageDiv.className = msgClass;
  messageDiv.dataset.messageDate = formatMessageDate(data.created_at);

  function buildBubble(extraClass = "") {
    const bubble = document.createElement("div");
    bubble.className = outlineClass + (extraClass ? " " + extraClass : "");

    if (hasImages) {
      const topPart = document.createElement("div");
      topPart.className = "top-part-message";
      const imageBlock = window.renderMessageImage(data.images);
      topPart.appendChild(imageBlock);
      bubble.appendChild(topPart);
    }

    const bottomPart = document.createElement("div");
    bottomPart.className = "bottom-part-message";

    if (hasText) {
      bottomPart.insertAdjacentHTML('beforeend', `
        <div class="msg-text">
          <p>${data.message_text}</p>
        </div>
      `);
    }

    bottomPart.insertAdjacentHTML('beforeend', `
      <div class="data-message">
        <p>${formatMessageTime(data.created_at)}</p>
        <img src="${checkReadIconPath}" alt="check_read">
      </div>
    `);

    bubble.appendChild(bottomPart);
    return bubble;
  }

  if (outlineClass === "message-outline" || isGroup === false) {
    messageDiv.appendChild(buildBubble());
  } else {
    const avatarSrc = '/static/chat_app/images/alert_conteiner/avatar-chat.png';

    const wrapper = document.createElement("div");
    wrapper.className = "div-outline-group-msg";

    const avatarDiv = document.createElement("div");
    avatarDiv.className = "avatar-message";
    avatarDiv.innerHTML = `<img src="${avatarSrc}">`;

    const bubble = buildBubble("change-dir");

    bubble.insertAdjacentHTML('afterbegin', `
      <div class="nick-data"><p>${username}</p></div>
    `);

    wrapper.appendChild(avatarDiv);
    wrapper.appendChild(bubble);
    messageDiv.appendChild(wrapper);
  }

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
      fragment.appendChild(renderMessage(message, message.sender, data.is_group))
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