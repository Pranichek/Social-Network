from user_app.models import User
from ..models import Chat
from user_app.services.friends_queries import get_friends
from chat_app.consumers import OnlineStatusConsumer


from django.template.loader import render_to_string
from django.http import JsonResponse, HttpRequest
from django.core.cache import cache


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
    last_messages = chat.messages.select_related('sender').order_by('-created_at')[:10]

    render_messages_html = render_to_string(
        "chat_app/particles/html_parts/messages_list.html",
        {
            "messages": reversed(last_messages),
            "current_user_id": current_user.id
        }
    )

    chat_card_html = render_to_string(
        "chat_app/particles/html_parts/chat_card.html",
        {
            "chat_user": other_user
        }
    )

    is_online = OnlineStatusConsumer.is_online(other_user.id)
    
    return JsonResponse({
        "success": True, 
        "chat_id": chat.id,
        "html": render_messages_html,
        "chat_card_html": chat_card_html, 
        'is_online': is_online,
        'chat_members': [other_user.id],
        'is_group': False
    })
