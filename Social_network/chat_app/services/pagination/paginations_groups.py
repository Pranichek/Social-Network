from chat_app.models import Chat


from django.http import JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string

def paginate_group_chats(request: HttpRequest):
    page_number = request.GET.get('page', 1)
    
    group_chats_list = Chat.objects.filter(
        users=request.user,
        is_group=True
    ).order_by('-id') 
    
    paginator = Paginator(group_chats_list, 10) 
    
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({
            'html': '',
            'has_next': False
        })

    html = render_to_string(
        'chat_app/particles/html_parts/group_chats_list.html', 
        {'group_chat': page_obj.object_list}, 
        request=request
    )

    return JsonResponse({
        'html': html,
        'has_next': page_obj.has_next()
    })