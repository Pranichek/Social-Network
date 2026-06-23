from ...models import Chat, Message
from ...socket_client import cloudinary_url_from_field

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpRequest
from django.utils import timezone 


def message_paginator(request: HttpRequest, chat_id: int):
    if not Chat.objects.filter(id=chat_id, users=request.user).exists():
            return JsonResponse({"success": False}, status=403)

    query = Message.objects.filter(chat_id=chat_id)\
        .select_related("sender")\
        .prefetch_related("images")\
        .order_by("-created_at", "-id")
    
    page_obj = Paginator(query, 10).get_page(request.GET.get("page", 1))
    messages = list(page_obj.object_list)[::-1]

    return JsonResponse(
        {
            "success": True,
            "messages": [
                {
                    "id": message.id,
                    "message_text": message.text,
                    "sender": message.sender.userprofile.pseudonym if message.sender else "Невідомий",
                    "is_current_user": message.sender.id == request.user.id,
                    "created_at": timezone.localtime(message.created_at).isoformat(),
                    "images": [cloudinary_url_from_field(img.image) for img in message.images.all()]
                }
                for message in messages
            ],
            "has_next": page_obj.has_next(),
            "is_group": Chat.objects.filter(id=chat_id, users=request.user).first().is_group
        }
    )