# from ..models import Chat, Message, MessageImage


# from django.http import JsonResponse
# from django.http import HttpRequest
# from django.utils import timezone 
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# def message_images(request: HttpRequest, chat_id: int):
#     if not Chat.objects.filter(id= chat_id, users= request.user).exists():
#         return JsonResponse({
#             'success': False
#         }, status= 403) 
    
#     text = request.POST.get('text', "").strip()
#     images = request.FILES.getlist('images')

#     if not text and not images:
#         return JsonResponse({
#             'success': False
#         }, status= 400)
    
#     message = Message.objects.create(
#         chat_id= chat_id,
#         sender= request.user,
#         text= text
#     )

#     for image in images:
#         MessageImage.objects.create(message= message, image= image)

#     image_urls = [image.image.url for image in message.images.all()]

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f'chat_{chat_id}',
#         {
#             'type': 'send_chat_message',
#             'id': message.id,
#             'message_text': message.text,
#             'sender': message.sender.userprofile.pseudonym,
#             'created_at': timezone.localtime(message.created_at).isoformat(),
#             'images': image_urls,
#             'is_current_user': True,
#         }
#     )
#     return JsonResponse({
#         'success': True
#     })

from ..models import Chat, Message, MessageImage
from ..socket_client import sio, background_loop

from django.http import JsonResponse
from django.http import HttpRequest
from django.utils import timezone 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..socket_client import cloudinary_url_from_field
import asyncio

# def message_images(request: HttpRequest, chat_id: int):
#     if not Chat.objects.filter(id=chat_id, users=request.user).exists():
#         return JsonResponse({'success': False}, status=403) 
    
#     text = request.POST.get('text', "").strip()
#     images = request.FILES.getlist('images')

#     if not text and not images:
#         return JsonResponse({'success': False}, status=400)
    
#     message = Message.objects.create(
#         chat_id=chat_id,
#         sender=request.user,
#         text=text
#     )

#     for image in images:
#         MessageImage.objects.create(message=message, image=image)

#     # image_urls = [img.image.url for img in message.images.all()]
#     image_urls = [cloudinary_url_from_field(img.image) for img in message.images.all()]


#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f'chat_{chat_id}',
#         {
#             'type': 'send_chat_message',
#             'message_id': message.id,        
#             'message_text': message.text,
#             'sender': message.sender.userprofile.pseudonym,
#             'created_at': timezone.localtime(message.created_at).isoformat(),
#             'images': image_urls,
#             'is_current_user': True,
#         }
#     )
#     return JsonResponse({'success': True})

def message_images(request: HttpRequest, chat_id: int):
    if not Chat.objects.filter(id=chat_id, users=request.user).exists():
        return JsonResponse({'success': False}, status=403) 
    
    text = request.POST.get('text', "").strip()
    images = request.FILES.getlist('images')

    if not text and not images:
        return JsonResponse({'success': False}, status=400)
    
    message = Message.objects.create(
        chat_id=chat_id,
        sender=request.user,
        text=text
    )

    for image in images:
        MessageImage.objects.create(message=message, image=image)

    image_urls = [cloudinary_url_from_field(img.image) for img in message.images.all()]

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{chat_id}',
        {
            'type': 'send_chat_message',
            'message_id': message.id,        
            'message_text': message.text or '',
            'sender': message.sender.userprofile.pseudonym,
            'created_at': timezone.localtime(message.created_at).isoformat(),
            'images': image_urls,
        }
    )

    chat = Chat.objects.get(id=chat_id)
    for user in chat.users.all():
        async_to_sync(channel_layer.group_send)(
            f'unread_{user.id}',
            {'type': 'unread_update'}
        )

    if background_loop:
        payload = {
            "type": "message:new",
            "chatId": str(chat_id),
            "message": {
                "id": message.id,
                "text": text,
                "sender": request.user.userprofile.pseudonym,
                "created_at": timezone.localtime(message.created_at).isoformat(),
                "images": image_urls,
            }
        }
        asyncio.run_coroutine_threadsafe(
            sio.emit("django_event", payload, namespace="/django-bridge"),
            background_loop
        )

    return JsonResponse({'success': True})