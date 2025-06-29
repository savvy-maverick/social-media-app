from .models import Notification
from post.models import Post
from account.models import FriendshipRequest

# create_notification(request, 'post_like')



def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    if type_of_notification == 'post_like':
        body = f'{request.user.name} liked one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} commented on one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'new_friendrequest':
        body = f'{request.user.name} sent you a friend request!'
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
    elif type_of_notification == 'accepted_friendrequest':
        body = f'{request.user.name} accepted your friend request!'
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
    elif type_of_notification == 'rejected_friendrequest':
        body = f'{request.user.name} rejected your friend request'
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for

    notification = Notification.objects.create(
        body = body,
        created_by = request.user,
        type_of_notification = type_of_notification,
        post_id=post_id,
        created_for= created_for
    )

    return notification