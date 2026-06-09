from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ..models import Chat

def create_group_service(request: HttpRequest):
    name = request.POST.get('name')
    user_ids = request.POST.getlist('users') 
    
    if not name or not user_ids:
        return JsonResponse({'success': False, 'error': 'Некоректні дані'}, status=400)

    chat = Chat.objects.create(name=name, is_group=True)
    
    chat.users.add(request.user)
    for user_id in user_ids:
        chat.users.add(user_id)
        
    return JsonResponse({
        'success': True, 
        'chat_id': chat.id, 
        'name': chat.name
    })


def open_chat_by_id_service(request: HttpRequest, chat_id: int):
    chat = get_object_or_404(Chat, id=chat_id, users=request.user)
    
    last_messages = chat.messages.select_related('sender').order_by('-created_at')[:20]

    render_messages_html = render_to_string(
        "chat_app/particles/messages_list.html",
        {
            "messages": reversed(last_messages),
            "current_user_id": request.user.id
        }
    )

    return JsonResponse({
        'success': True,
        'chat_id': chat.id,
        'html': render_messages_html
    })