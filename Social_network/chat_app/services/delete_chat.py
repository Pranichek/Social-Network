from django.http import JsonResponse, HttpRequest
from ..models import Chat

def delete_chat(request: HttpRequest, chat_id: int):
    chat = Chat.objects.get(id=chat_id)
    
    if not chat:
        return JsonResponse(
            {
                'success': False
            }
        )
    
    if request.user not in chat.users.all():
        return JsonResponse(
            {
                'success': False
            }
        )
    
    chat.delete()
    return JsonResponse(
        {
            'success': True
        }
    )