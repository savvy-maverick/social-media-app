from django.db import models
import uuid

from account.models import User
from post.models import Post


# Create your models here.

class Notification(models.Model):
    NEWFRIENDREQUEST = 'new_friendrequest'
    ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
    REJECTEDFRIENDREQUEST = 'rejected_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friendrequest'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
        (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment')
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    created_at = models.DateTimeField(auto_now_add=True)

