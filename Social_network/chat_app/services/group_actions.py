from ..models import Chat
from chat_app.consumers import OnlineStatusConsumer
from ..forms import GroupChatUpdateForm


from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string


def create_group_service(request: HttpRequest):
    name = request.POST.get('name')
    user_ids = request.POST.getlist('users') 
    
    if not name or not user_ids:
        return JsonResponse({'success': False, 'error': 'Некоректні дані'}, status=400)

    chat = Chat.objects.create(
        name=name, 
        is_group=True,
        admin = request.user
    )
        
    chat.users.add(request.user)
    chat.users.add(*user_ids)
        
    return JsonResponse({
        'success': True, 
        'chat_id': chat.id, 
        'name': chat.name
    })


def open_chat_by_id_service(request: HttpRequest, chat_id: int):
    chat = get_object_or_404(Chat, id=chat_id, users=request.user)
    
    last_messages = chat.messages.select_related('sender').order_by('-created_at')[:20]

    render_messages_html = render_to_string(
        "chat_app/particles/html_parts/messages_list.html",
        {
            "messages": reversed(last_messages),
            "current_user_id": request.user.id
        }
    )

    user_ids = list(chat.users.values_list('id', flat=True))
    count_online = OnlineStatusConsumer.get_online_count(user_ids)

    return JsonResponse({
        'success': True,
        'chat_id': chat.id,
        'html': render_messages_html,
        'chat_members': user_ids,
        "is_group": True,
        'online_count': count_online
    })

# редагування групи
def update_group_service(request: HttpRequest, chat_id: int):
    chat: Chat = Chat.objects.get(id= chat_id, is_group= True)

    if not chat.exists():
        return JsonResponse({
            'success': False
        }, status= 404)
    
    if chat.admin != request.user:
        return JsonResponse({
            'success': False
        }, status= 403)
    
    
    form = GroupChatUpdateForm(request.POST, request.FILES, instance= chat)
    
    if form.is_valid():
        group = form.save(commit=False)
        group.save()
        new_users = form.cleaned_data['users']
        chat.users.set(new_users)
        chat.user.add(request.user)
        return JsonResponse({
            'success': True,
            'chat_id': chat.id,
            'name': chat.name,
            
       })
    
    return JsonResponse({
        'success': False,
        
    }, status =  400)
    
    