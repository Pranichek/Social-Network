from chat_app.models import Chat, Message

from django.db.models import OuterRef, Subquery
from django.http import JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string
from django.utils import timezone


def paginate_group_chats(request: HttpRequest):
    page_number = request.GET.get('page', 1)

    last_message = Message.objects.filter(
        chat=OuterRef('pk')
    ).order_by('-created_at')

    group_chats_list = Chat.objects.filter(
        users=request.user,
        is_group=True
    ).annotate(
        last_message_text=Subquery(last_message.values('text')[:1]),
        last_message_data=Subquery(last_message.values('created_at')[:1])
    ).order_by('-id') 
    
    paginator = Paginator(group_chats_list, 10)
        
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'html': '', 'has_next': False})

    for chat in page_obj.object_list:
        if chat.last_message_data:
            chat.last_message_data = timezone.localtime(chat.last_message_data)

    html = render_to_string(
        'chat_app/particles/html_parts/group_chats_list.html', 
        {'group_chat': page_obj.object_list}, 
        request=request
    )

    return JsonResponse({'html': html, 'has_next': page_obj.has_next()})