from django.http import JsonResponse
from django.core.mail import send_mail

from django.contrib.auth.forms import PasswordChangeForm

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm
from .models import FriendshipRequest, User
from .serializers import UserSerializer, FriendshipRequestSerializer
from notification.utils import create_notification



@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    }) 


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
       user = form.save()
       user.is_active = False
       user.save()

       url = f"http://127.0.0.1:8000/activateemail/?email={user.email}&id={user.id}"

       send_mail(
           "Please verify your email",
           f"The url for activating your account is: {url}",
           "noreply@wey.com",
           [user.email],
           fail_silently = False,
       )

        # send verification email later
    else:
        message = form.errors.as_json()
    
    print(data, message)

    return JsonResponse({'message':message})

@api_view(['GET'])
def friends(request, pk):
    user = request.user


    requests = FriendshipRequest.objects.filter(created_for=user, status= FriendshipRequest.SENT)
    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendshipRequestSerializer(requests, many=True).data

    })

@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')
    name = request.data.get('name')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    
    else:

        print(request.FILES)
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)

        return JsonResponse({'message':'Information updated', 'user': serializer.data  })
    

@api_view(['POST'])
def editpassword(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST, instance=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)





@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by= user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by= request.user)

    if not check1 or not check2:
        friendship_request = FriendshipRequest(created_for=user, created_by=request.user)
        friendship_request.save()

        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendship_request.id)
    else:
        return JsonResponse({'message': 'request already sent'})

    
    print('send request', pk)

    return JsonResponse({'message': 'friendship request created'} )

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by= user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return JsonResponse({'message': 'updated successfully'})

