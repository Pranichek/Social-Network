from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Chat
from django.http import HttpRequest


def message_paginator(request: HttpRequest, chat_id: int):
    chat = get_object_or_404(Chat, id=chat_id, users=request.user)
    messages_query = chat.messages.select_related('sender').order_by('-created_at')

    paginator = Paginator(messages_query, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    message_data = []
    target_user_id = None
    all_chat_users = chat.users.all()

    for user in all_chat_users:
        if user != request.user:
            target_user_id = user.id
            break  

    for message in reversed(page_obj.object_list):        
        if message.sender:
            sender_name = message.sender.username
        else:
            sender_name = 'Невідомий'
            
        if message.sender:
            sender_id = message.sender.id
        else:
            sender_id = None

        message_data.append({
            'sender': sender_name,
            'message_text': message.text,
            'other_user': sender_id,
            'user_id': target_user_id
        })
        
    return JsonResponse({
        "success": True,
        "messages": message_data,
        "has_next": page_obj.has_next()
    })