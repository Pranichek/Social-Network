from user_app.services.friends_queries import get_friends


from django.http import JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string


def paginate_contact(request: HttpRequest):
    page_number = request.GET.get('page', 1)
    friends_list = get_friends(request.user)
    
    paginator = Paginator(friends_list, 20)
    
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({
            'html': '',
            'has_next': False
        })

    html = render_to_string(
        'chat_app/particles/html_parts/contacts_list.html', 
        {'friends': page_obj.object_list}, 
        request=request
    )

    return JsonResponse({
        'html': html,
        'has_next': page_obj.has_next()
    })