from user_app.models import User
from chat_app.models import Chat

from django.http import JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string
from django.utils import timezone

def paginate_active_chats(request: HttpRequest):
    page_number = int(request.GET.get('page', 1))

    solo_chats = Chat.objects.filter(
        users=request.user,
        is_group=False
    ).prefetch_related('messages', 'users')

    active_chats_data = []

    for chat in solo_chats:
        other_user = chat.users.exclude(id=request.user.id).first()
        if not other_user:
            continue

        message = chat.messages.order_by('-created_at').first()

        if message:
            last_message_text = message.text if message.text else 'Зображення'
            last_message_data = timezone.localtime(message.created_at).strftime('%H:%M')
        else:
            last_message_text = 'Немає повідомлень'
            last_message_data = ''

        unread_count = chat.messages.exclude(
            sender=request.user
        ).exclude(
            readers=request.user
        ).count()

        active_chats_data.append({
            'user': other_user,
            'chat': chat,
            'last_message_text': last_message_text,
            'last_message_data': last_message_data,
            'unread_count': unread_count,
        })

    active_chats_data.sort(key=lambda x: x['unread_count'], reverse=True)

    paginator = Paginator(active_chats_data, 10)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'html': '', 'has_next': False})

    html = render_to_string(
        'chat_app/particles/html_parts/active_chats_list.html',
        {'active_chats': page_obj.object_list},
        request=request
    )

    return JsonResponse({'html': html, 'has_next': page_obj.has_next()})