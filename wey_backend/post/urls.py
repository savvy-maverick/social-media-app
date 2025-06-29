from django.urls import path
from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:pk>/like/', api.post_likes, name='post_likes'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('trends/', api.get_trends, name='get_trends'),
    path('trends/<int:pk>', api.get_trends_detail, name='get_trends_details'),


]