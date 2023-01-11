from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import *

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if PD.is_valid() and UD.is_valid():
            pw=UD.cleaned_data['password']
            UFO=UD.save(commit=False)
            UFO.set_password(pw)
            UFO.save()

            PFO=PD.save(commit=False)
            PFO.user=UFO
            PFO.save()

            send_mail('User registration',
            'Regiistration is success full',
            'narasar198@gmail.com',
            [UFO.email],fail_silently=False)


            return HttpResponse('registration is successsfull')
            
    return render(request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def profile_info(request):
    username=request.session.get('username')
    USD=User.objects.get(username=username)
    PFD=Profile.objects.get(user=USD)
    d={'USD':USD,'PFD':PFD}
    return render(request,'profile_info.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        npw=request.POST['npw']
        cpw=request.POST['cpw']
        if npw==cpw:
            USO=User.objects.get(username=username)
            USO.set_password(cpw)
            USO.save()
            return HttpResponseRedirect(reverse('user_login'))

    return render(request,'change_password.html')


def reset_password(request):
    # this is the reset or forgot password for user login
    if request.method=='POST':
        username=request.POST['username']
        npw=request.POST['npw']
        cpw=request.POST['cpw']
        if npw==cpw:
            LUSO=User.objects.filter(username=username)
            # it gives list of objects
            if LUSO:
                LUSO[0].set_password(cpw)
                LUSO[0].save()

                send_mail('change_password',
                'changing the password or RESET password is successfully changed',
                'narasar198@gmail.com',
                [LUSO[0].email],fail_silently=False)

                return HttpResponseRedirect(reverse('user_login'))
            else:
                return HttpResponse('this user is not available in my database')

    return render(request,'reset_password.html')
    