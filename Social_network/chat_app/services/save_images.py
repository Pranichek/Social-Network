from ..models import Chat, Message, MessageImage


from django.http import JsonResponse
from django.http import HttpRequest
from django.utils import timezone 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def message_images(request: HttpRequest, chat_id: int):
    if not Chat.objects.filter(id= chat_id, users= request.user).exists():
        return JsonResponse({
            'success': False
        }, status= 403) 
    
    text = request.POST.get('text', "").strip()
    images = request.FILES.getlist('images')

    if not text and not images:
        return JsonResponse({
            'success': False
        }, status= 400)
    
    message = Message.objects.create(
        chat_id= chat_id,
        sender= request.user,
        text= text
    )

    for image in images:
        MessageImage.objects.create(message= message, image= image)

    image_urls = [image.image.url for image in message.images.all()]

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{chat_id}',
        {
            'type': 'send_chat_message',
            'id': message.id,
            'message_text': message.text,
            'sender': message.sender.userprofile.pseudonym,
            'created_at': timezone.localtime(message.created_at).isoformat(),
            'images': image_urls,
            'is_current_user': True,
        }
    )
    return JsonResponse({
        'success': True
    })