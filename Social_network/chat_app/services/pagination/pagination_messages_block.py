from user_app.models import User


from django.http import JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string

def paginate_active_chats(request: HttpRequest):
    page_number = request.GET.get('page', 1)
    
    active_chats_list = User.objects.filter(
        chats__users=request.user,
        chats__is_group=False
    ).exclude(
        id=request.user.id
    ).select_related(
        'userprofile' 
    ).distinct().order_by('-id') 
    
    print("lolololo")
    print(len(active_chats_list))

    paginator = Paginator(active_chats_list, 10) 
    
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({
            'html': '',
            'has_next': False
        })

    html = render_to_string(
        'chat_app/particles/html_parts/active_chats_list.html', 
        {'active_chats': page_obj.object_list}, 
        request=request
    )

    return JsonResponse({
        'html': html,
        'has_next': page_obj.has_next()
    })