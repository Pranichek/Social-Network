let currentChatPage = 1
let isChatLoading = false
let activeChatId = null

const messageList = document.querySelector("#messeages")
let chatSentinel = document.getElementById("chat-load-sentinel")

const chatObserver = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && isChatLoading == false && activeChatId) {
    isChatLoading = true
    currentChatPage++
    
    const previousScrollHeight = messageList.scrollHeight

    const response = await fetch(
      `/chat/${activeChatId}/messages/?page=${currentChatPage}`,
      {
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      }
    )
    
    const data = await response.json()

    if (data.success && data.messages.length > 0) {
      let htmlString = ""
      data.messages.forEach(message => {
        let msgClass = (message.other_user == message.user_id) ? "message other_user" : "message"
        const checkReadIconPath = '/static/chat_app/images/chat_images/check_read.svg'
        if (msgClass == "message"){
          
          htmlString += `
                <div class="${msgClass}">
                  <div class="message-outline">
                      <div class="msg-text">
                          <p>${message.message_text}</p>
                      </div>
                      
                      <div class="data-message">
                          <p>10:01</p>
                          <img src= "${checkReadIconPath}" alt="check_read">
                      </div>
                  </div>
                </div>
              `
        }else{
          // htmlString += `<div class="${msgClass}">${message.sender}: ${message.message_text}</div>`

          htmlString += `
            <div class="${msgClass}">

              <div class="other-message-outline">

                  <div class="msg-text">
                      <p>${message.message_text}</p>
                  </div>
                  
                  <div class="data-message">
                      <p>10:01</p>
                      <img src= "${checkReadIconPath}" alt="check_read">
                  </div>

              </div>

            </div>
          `
          
        }
      })
      
      chatSentinel = document.getElementById("chat-load-sentinel")
      
      if (chatSentinel) {
        chatSentinel.insertAdjacentHTML("afterend", htmlString)
      }
      
      messageList.scrollTop = messageList.scrollHeight - previousScrollHeight
    }

    if (!data.has_next) {
      chatObserver.disconnect()
      if (chatSentinel) chatSentinel.remove()
    }

    isChatLoading = false
  }
}, {
  root: messageList,
  rootMargin: "20px"
})