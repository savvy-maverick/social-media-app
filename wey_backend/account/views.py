from django.shortcuts import render
from .models import User
from django.http import HttpResponse

# Create your views here.


def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()

        print(user)

        return HttpResponse('Your account has been activated, you can login now')
    
    else:
        return HttpResponse('The parameters is not valid!')

