from user_app.models import Friendship
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def add_friend_request(current_user, other_user):
    Friendship.objects.get_or_create(
        from_user = current_user,
        to_user = other_user,
        defaults = {'status': 'pending'}
    )

    async_to_sync(channel_layer.group_send)(
        f"friend_request_{other_user.id}",
        {
            "type": "friend_request_update",
            "from_user_id": current_user.id,
            "pseudonym": current_user.userprofile.pseudonym,
            "username": current_user.username,
        }
    )

    return {'label': 'Очікування'}


def dismiss_recommendation(current_user, other_user):
    Friendship.objects.get_or_create(
        from_user = current_user,
        to_user = other_user,
        defaults = {'status': 'dismissed'}
    )

    return {
        'remove': True
    }


def accept_friend_request(current_user, other_user):
    friendship = Friendship.objects.filter(
        from_user = other_user,
        to_user = current_user
    ).first()

    friendship.status = 'accepted'

    friendship.save()
    
    async_to_sync(channel_layer.group_send)(
        f"friend_request_{current_user.id}",
        {
            "type" : "friend_request_update",
            
        }
    )

    async_to_sync(channel_layer.group_send)(
        f"friend_request_{other_user.id}",
        {
            "type" : "friend_request_update",
            
        }
    )

    return {
        'remove': True,
        'friend': other_user
    }

def any_delete(current_user, to_user):
    friendship = Friendship.objects.filter(
        from_user = current_user,
        to_user = to_user
    ).first()

    if not friendship:
        friendship = Friendship.objects.filter(
            from_user = to_user,
            to_user = current_user
        ).first()

    async_to_sync(channel_layer.group_send)(
        f"friend_request_{current_user.id}",
        {
            "type" : "friend_request_update",
            
        }
    )

    if friendship:
        
        if friendship.status == 'accepted' or friendship.status == "pending":
            friendship.delete()

        return {
            'remove': True
        }
    else:
        Friendship.objects.get_or_create(
            from_user = current_user,
            to_user = to_user,
            defaults = {'status': 'dismissed'}
        )

        return {
            'remove': False
        }

    


# def delete_friendship(current_user, to_user):
#     friendship = Friendship.objects.filter(
#         from_user = current_user,
#         to_user = to_user
#     ).first()

#     if not friendship:
#         friendship = Friendship.objects.filter(
#             from_user = to_user,
#             to_user = current_user
#         ).first()

#     if friendship:
#         friendship.delete()

#     return {
#         'remove': True
#     }
    
