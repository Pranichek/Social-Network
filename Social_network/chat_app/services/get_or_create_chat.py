from user_app.models import User
from ..models import Chat
from user_app.services.friends_queries import get_friends


from django.http import JsonResponse, HttpRequest


def get_or_create_chat(request: HttpRequest, user_id: int):
    current_user = request.user
    other_user = User.objects.get(id = user_id)
    friends = get_friends(current_user=current_user)

    if other_user not in friends:
        return JsonResponse({
            'success': False,
        }, status = 403)
    
    user_chat_ids = Chat.objects.filter(users = current_user, is_group = False).values_list("id", flat = True)
    chat = Chat.objects.filter(id__in = user_chat_ids, users = other_user, is_group = False).first()

    if chat is None:
        chat = Chat.objects.create(is_group = False)
        chat.users.add(current_user, other_user)

    # [:20] - робимо зріз масиву, щоб передавали максимум 20 повідомлень
    last_messages = chat.messages.select_related('sender').order_by('-created_at')[:20]
    message_data = []
    
    for message in reversed(last_messages):
        if message.sender:
            sender_name = message.sender.username
        else:
            sender_name = 'Невідомий'

        message_data.append({
            'sender': sender_name,
            'message_text': message.text,
            "other_user": message.sender.id,
            "user_id": user_id
        })
    return JsonResponse({
        "success": True, 
        "chat_id": chat.id,
        "messages": message_data
    })
