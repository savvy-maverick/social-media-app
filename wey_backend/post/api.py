from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Post, Like, Comment
from account.models import User
from .forms import PostForm
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from account.serializers import UserSerializer

# Create your views here.

@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)
    posts = Post.objects.filter(created_by__id__in = list(user_ids))

    serializer = PostSerializer(posts, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })



@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(created_by_id=id)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
        'posts': post_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)
    
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    
    else:
        return JsonResponse({'error': 'add something later'})
        


@api_view(['POST'])
def post_likes(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(created_by=request.user):

        like = Like.objects.create(created_by=request.user)
    
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'Already liked this'})
    

@api_view(['POST'])
def post_create_comment(request, pk):
    
    comment = Comment.objects.create(body= request.data.get('body'), created_by= request.user)
    serializer = CommentSerializer(comment)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()



    print(request.data)

    return JsonResponse(serializer.data, safe=False)

    


